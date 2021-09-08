from reranker_pb2_grpc import RerankerServicer
from abc import ABC, abstractmethod

class AbstractReranker(ABC, RerankerServicer):

    @abstractmethod
    def rerank(self, rerank_request, context):
        """
        Takes in a rerank_request (search result and reranker)
        and reranks the resul
        """
        pass