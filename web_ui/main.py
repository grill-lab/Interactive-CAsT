from flask import Flask, render_template, request
import os

import time
import json

import sys
import grpc

sys.path.insert(0, '/shared')
sys.path.insert(0, '/shared/compiled_protobufs')


from search_result_pb2 import SearchResult
from searcher_pb2 import SearchQuery, DocumentQuery
from searcher_pb2_grpc import SearcherStub

from reranker_pb2 import RerankRequest
from reranker_pb2_grpc import RerankerStub

from rewriter_pb2 import RewriteRequest
from rewriter_pb2_grpc import RewriterStub

from utils.conversion_utils import context_converter
from google.protobuf.json_format import MessageToDict

app = Flask(__name__)


searcher_channel = grpc.insecure_channel(os.environ['SEARCHER_URL'])
search_client = SearcherStub(searcher_channel)

reranker_channel = grpc.insecure_channel(os.environ['RERANKER_URL'])
rerank_client = RerankerStub(reranker_channel)

rewriter_channel = grpc.insecure_channel(os.environ['REWRITER_URL'])
rewrite_client = RewriterStub(rewriter_channel)

@app.route('/')
def display_homepage():
    return render_template("homepage.html")

@app.route('/<id>/fulltext')
def display_doc(id):

    args = request.args
    document_query = DocumentQuery()

    if args.get("search_backend"):
        if args["search_backend"] == "pyserini":
            document_query.search_backend = 0
    
    document_query.document_id = id
    retrieved_document = search_client.get_document(document_query)

    converted_document = MessageToDict(retrieved_document)

    return render_template("fulltext.html", doc = converted_document)



@app.route('/search')
def search():
    
    args = request.args

    search_query = SearchQuery()
    search_query.query = args["query"].replace("_", " ")
    search_query.num_hits = int(args["numDocs"])
    search_query.search_parameters.parameters["b"] = args["b"]
    search_query.search_parameters.parameters["k1"] = args["k1"]

    if args["backend"] == "Pyserini":
        search_query.search_backend = 0
    
    if args["collection"] == "ALL":
        search_query.search_parameters.collection = 0
    elif args["collection"] == "KILT":
        search_query.search_parameters.collection = 1
    elif args["collection"] == "MARCO":
        search_query.search_parameters.collection = 2
    elif args["collection"] == "WAPO":
        search_query.search_parameters.collection = 3

    start_time = time.time()
    search_result = search_client.search(search_query)

    passage_limit = int(args["passageCount"])

    if args["skipRerank"] == "true":
        
        documents = []
        for document in search_result.documents:
            converted_document = MessageToDict(document)
            converted_document['passages'] = converted_document['passages'][:passage_limit]
            documents.append(converted_document)
        
        end_time = time.time()
        duration = int(end_time - start_time)
        
        return render_template("results.html", docs = documents, 
            numFound=len(documents), duration=duration, query=search_query.query)
    
    rerank_request = RerankRequest()
    rerank_request.search_query = search_query.query

    rerank_request.num_passages = int(args["passageLimit"])
    rerank_request.search_result.MergeFrom(search_result)

    rerank_result = rerank_client.rerank(rerank_request)
    
    documents = []
    for document in rerank_result.documents:
        converted_document = MessageToDict(document)
        converted_document['passages'] = converted_document['passages'][:passage_limit]
        documents.append(converted_document)
        
    end_time = time.time()
    duration = int(end_time - start_time)
        
    return render_template("results.html", docs = documents, 
        numFound=len(documents), duration=duration, query=search_query.query)


@app.route('/rewrite', methods=['POST'])
def rewrite():

    client_rewrite_request = request.get_data()
    client_rewrite_request = json.loads(client_rewrite_request)

    rewrite_request = RewriteRequest()
        
    rewrite_request.search_query = client_rewrite_request["searchQuery"]

    if client_rewrite_request["turnsToUse"] == "raw":
        rewrite_request.query_context = client_rewrite_request["context"]
        
    else:
        rewrite_request.query_context = context_converter(client_rewrite_request["context"], 
            int(client_rewrite_request["turnsToUse"]))
        

    if client_rewrite_request["rewriter"] == "T5":
        rewrite_request.rewriter = 0

    rewrite_result = rewrite_client.rewrite(rewrite_request)
    
    return {
        'rewrite' : rewrite_result.rewrite, 
        'context' : rewrite_request.query_context
    }




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))