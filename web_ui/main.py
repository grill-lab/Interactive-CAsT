from flask import Flask, render_template, request, jsonify
import os

import time
import json
import logging
import sys
import grpc

sys.path.insert(0, '/shared')
sys.path.insert(0, '/shared/compiled_protobufs')


from search_result_pb2 import SearchResult
from searcher_pb2 import SearchQuery, DocumentQuery
from searcher_pb2_grpc import SearcherStub

from reranker_pb2 import RerankRequest
from reranker_pb2_grpc import RerankerStub

from utils.conversion_utils import context_converter
from google.protobuf.json_format import MessageToDict

app = Flask(__name__)

options = (
    ('grpc.max_message_length', 1000 * 1024 * 1024), 
    ('grpc.max_receive_message_length', 1000 * 1024 * 1024),
    ('grpc.max_send_message_length', 1000 * 1024 * 1024)
)
searcher_channel = grpc.insecure_channel(os.environ['SEARCHER_URL'], options = options)
search_client = SearcherStub(searcher_channel)

reranker_channel = grpc.insecure_channel(os.environ['RERANKER_URL'], options = options)
rerank_client = RerankerStub(reranker_channel)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'You found the comets endpoint home page!'})

@app.route('/save', methods=['POST', 'GET'])
def save():
    data = request.get_json()
    file_name = data["filename"]
    contents = data["contents"]

    with open(f"file_system/{file_name}", "w") as json_file:
        json.dump(contents, json_file, indent=4)
    
    return jsonify({
        "message" : f"{file_name} saved to File System"
    })

@app.route('/load', methods=['GET', 'POST'])
def load():
    data = request.get_json()
    file_name = data["filename"]

    with open(f"file_system/{file_name}") as json_file:
        json_contents = json.load(json_file)
    
    return jsonify({
        "filename" : file_name,
        "contents" : json_contents
    })




@app.route('/search', methods=['POST', 'GET'])
def search():

    data = request.get_json()
    search_query = SearchQuery()

    search_query.query = data["query"]
    search_query.num_hits = 100
    search_query.search_parameters.parameters["b"] = "0.4" #"0.82"
    search_query.search_parameters.parameters["k1"] = "0.9" #"4.46"

    search_query.search_parameters.parameters["set_rm3"] = str(data.get("set_rm3", "False"))

    if not data.get("type") or data.get("type") == "hybrid":
        search_query.searcher_type = 2 # Hybrid Search
    elif data.get("type") == "sparse":
        search_query.searcher_type = 0 # Sparse Search
    elif data.get("type") == "dense":
        search_query.searcher_type = 1

    # DOCUMENTS SEARCH
    search_query.search_parameters.collection = 0
    search_result = search_client.search(search_query)

    print("Doc Search done")

    documents = []
    if data.get("rerank") or data.get("rerank") == None:
        rerank_request = RerankRequest()
        rerank_request.search_query = search_query.query
        rerank_request.num_passages = 20
        rerank_request.num_docs = 100
        rerank_request.search_result.MergeFrom(search_result)
        rerank_result = rerank_client.rerank(rerank_request)
        
        
        for document in rerank_result.documents:
            converted_document = MessageToDict(document)
            converted_document['contents'] = converted_document['passages'][0]['body']
            del converted_document['passages']
            documents.append(converted_document)
    else:
        for document in search_result.documents:
            converted_document = MessageToDict(document)
            converted_document['contents'] = converted_document['passages'][0]['body']
            del converted_document['passages']
            documents.append(converted_document)

        print("Docs reranked")
    
    # ENTITIES SEARCH
    search_query.searcher_type = 0 # Always Sparse Search
    search_query.search_parameters.collection = 4
    search_result = search_client.search(search_query)

    print("Entity Search done")

    entities = []
    if data.get("rerank") or data.get("rerank") == None: # This way because 
        rerank_request.search_result.Clear()
        rerank_request.search_result.MergeFrom(search_result)
        rerank_result = rerank_client.rerank(rerank_request)

        for entity in rerank_result.documents:
            converted_entity = MessageToDict(entity)
            converted_entity['contents'] = converted_entity['passages'][0]['body']
            del converted_entity['passages']
            entities.append(converted_entity)
    else:
        for entity in search_result.documents:
            converted_entity = MessageToDict(entity)
            converted_entity['contents'] = converted_entity['passages'][0]['body']
            del converted_entity['passages']
            entities.append(converted_entity)
        
        print("Entities reranked")


    return jsonify(
        {
            "documents" : documents[:int(data["k"])],
            "entities" : entities[:int(data["k"])]
        }
    )

@app.route('/get_documents', methods=['POST', 'GET'])
def get_documents():

    data = request.get_json()
    doc_ids = data["doc_ids"]
    entity_ids = data["entity_ids"]
    document_query = DocumentQuery()
    document_query.searcher_type = 0 # Use the Sparse Searcher

    retrieved_documents = []
    document_query.collection = 0
    for doc_id in doc_ids:
        try:
            document_query.document_id = doc_id
            retrieved_document = search_client.get_document(document_query)
            converted_document = MessageToDict(retrieved_document)
            converted_document["contents"] = converted_document["passages"][0]["body"]
            del converted_document["passages"]
            retrieved_documents.append(converted_document)
        except:
            continue

    retrieved_entities = []
    document_query.collection = 4
    for entity_id in entity_ids:
        try:
            document_query.document_id = entity_id
            retrieved_document = search_client.get_document(document_query)
            converted_document = MessageToDict(retrieved_document)
            converted_document["contents"] = converted_document["passages"][0]["body"]
            del converted_document["passages"]
            retrieved_entities.append(converted_document)
        except:
            continue
    
    return jsonify({
        "documents" : retrieved_documents,
        "entities" : retrieved_entities
    })



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))