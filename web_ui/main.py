# import sys
# import grpc

# sys.path.insert(0, '/shared')
# sys.path.insert(0, '/shared/compiled_protobufs')

# from searcher_pb2 import SearchQuery, DocumentQuery
# from searcher_pb2_grpc import SearcherStub

# from reranker_pb2 import RerankRequest
# from reranker_pb2_grpc import RerankerStub

# from search_result_pb2 import SearchResult

# # ---------------

# searcher_channel = grpc.insecure_channel("http://searcher:8000")
# search_client = SearcherStub(searcher_channel)

# reranker_channel = grpc.insecure_channel("http://reranker:8000")
# rerank_client = RerankerStub(reranker_channel)

# # ----------------

# search_query = SearchQuery()
# search_query.query = "Rock paper scissors"

# search_query.search_parameters.collection = 1
# search_query.num_hits = 10

# document_query = DocumentQuery()
# document_query.document_id = "KILT_59729086"

# search_result = search_client.search(search_query)
# document_result = search_client.get_document(document_query)

# # print(search_result)

# # ------------------- if we want to rerank

# rerank_request = RerankRequest()
# rerank_request.search_query = search_query.query
# rerank_request.num_passages = 4
# rerank_request.search_result.MergeFrom(search_result)

# rerank_result = rerank_client.rerank(rerank_request)
# print(rerank_result)

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'