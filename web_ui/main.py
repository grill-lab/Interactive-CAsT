from flask import Flask
import os

app = Flask(__name__)

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

# ---------------

searcher_channel = grpc.insecure_channel(os.environ['SEARCHER_URL'])
search_client = SearcherStub(searcher_channel)

reranker_channel = grpc.insecure_channel(os.environ['RERANKER_URL'])
rerank_client = RerankerStub(reranker_channel)

rewriter_channel = grpc.insecure_channel(os.environ['REWRITER_URL'])
rewrite_client = RewriterStub(rewriter_channel)

@app.route('/test')
def test():

    

    # ----------------

    search_query = SearchQuery()
    search_query.query = "Rock paper scissors"

    search_query.search_parameters.collection = 1
    search_query.num_hits = 10

    document_query = DocumentQuery()
    document_query.document_id = "KILT_59729086"

    search_result = search_client.search(search_query)
    document_result = search_client.get_document(document_query)

    # print(search_result)

    # ------------------- if we want to rerank

    rerank_request = RerankRequest()
    rerank_request.search_query = search_query.query
    rerank_request.num_passages = 4
    rerank_request.search_result.MergeFrom(search_result)

    # rerank_result = rerank_client.rerank(rerank_request)
    # print(rerank_result)


    # --------------------- testing rewritng

    rewrite_request = RewriteRequest()
    rewrite_request.search_query = 'How do I get one'
    rewrite_request.query_context = "I bought a pizza last week"
    rewrite_result = rewrite_client.rewrite(rewrite_request)
    
    return rewrite_result.rewrite


@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=7000, debug=True)
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    #app.run()