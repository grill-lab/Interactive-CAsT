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

    @abstractmethod
    def convert_search_response(self, search_hits):
        """
        Takes the results from a search backend and converts it to 
        the Document protocol buffer.
        """

        pass