import sys

sys.path.insert(0, '/shared')
sys.path.insert(0, '/shared/compiled_protobufs')

import grpc
from concurrent import futures

from summarisers import BARTSummariser as SummariserServicer
from summariser_pb2_grpc import add_SummariserServicer_to_server

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options = (('grpc.max_receive_message_length', 2000 * 1024 * 1024),('grpc.max_message_length', 2000 * 1024 * 1024), ('grpc.max_send_message_length', 2000 * 1024 * 1024))
    )
    add_SummariserServicer_to_server(SummariserServicer(), server)

    server.add_insecure_port("[::]:8000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()