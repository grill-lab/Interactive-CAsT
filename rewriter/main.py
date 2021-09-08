import sys

sys.path.insert(0, '/shared')
sys.path.insert(0, '/shared/compiled_protobufs')

import grpc
from concurrent import futures

from rewriters import NeuralRewriter as RewriterServicer
from rewriter_pb2_grpc import add_RewriterServicer_to_server

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_RewriterServicer_to_server(RewriterServicer(), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()