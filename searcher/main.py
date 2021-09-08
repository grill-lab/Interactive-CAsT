import sys

sys.path.insert(0, '/shared')
sys.path.insert(0, '/shared/compiled_protobufs')

import grpc
from concurrent import futures

from searchers import PyseriniSearcher as SearcherServicer
from searcher_pb2_grpc import add_SearcherServicer_to_server

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_SearcherServicer_to_server(SearcherServicer(), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
