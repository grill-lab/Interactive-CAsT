from rewriter_pb2_grpc import RewriterServicer
from abc import ABC, abstractmethod

class AbstractRewriter(ABC, RewriterServicer):

    @abstractmethod
    def rewrite(self, rewrite_request, context):
        """
        Takes in a rerank_request (search result and reranker)
        and reranks the resul
        """
        pass