from summariser_pb2_grpc import SummariserServicer
from abc import ABC, abstractmethod

class AbstractSummariser(ABC, SummariserServicer):

    @abstractmethod
    def summarise(self, summary_request, context):
        """
        Takes in a summary_request (search result and summariser)
        and generates a summary
        """
        pass