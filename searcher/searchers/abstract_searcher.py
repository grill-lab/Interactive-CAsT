from searcher_pb2_grpc import SearcherServicer
from abc import ABC, abstractmethod

class AbstractSearcher(ABC, SearcherServicer):
    
    @abstractmethod
    def search(self, search_query, context):
        """
        Query an index and return search results
        """
        pass

    @abstractmethod
    def get_document(self, document_request, context):
        """
        Given a document id, return a document's attributes
        """

        pass