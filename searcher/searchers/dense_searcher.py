from .abstract_searcher import AbstractSearcher
from searcher_pb2 import SearchQuery, DocumentQuery
from search_result_pb2 import SearchResult, Document, Passage

from pyserini.dsearch import SimpleDenseSearcher
from .sparse_searcher import SparseSearcher
import logging

class DenseSearcher(AbstractSearcher):

    def __init__(self):

        self.indexes = {
            # not sure about efficacy of encoders yet.
            'ALL' : SimpleDenseSearcher('../../shared/indexes/dense/dense_test', 
                            'castorini/ance-msmarco-doc-firstp')
            # new indices go here
        }

        self.chosen_index = None
        self.sparse_searcher = SparseSearcher()
    
    def search(self, search_query: SearchQuery, context):

        query: str = search_query.query
        num_hits: int = search_query.num_hits

        logging.info("WE ARE USING THE DENSE SEARCHER")

        # we need a corresponing sparse searcher to retrieve doc attributes
        if search_query.search_parameters.collection == 0:
            self.chosen_index = self.indexes['ALL']
            self.sparse_searcher.chosen_index = self.sparse_searcher.indexes['ALL']
        
        hits = self.chosen_index.search(query, num_hits)
        search_result = SearchResult()

        for hit in hits:
            document_query = DocumentQuery()
            document_query.document_id = hit.docid
            document_query.searcher_type = 0

            retrieved_document = self.get_document(document_query, context)
            search_result.documents.append(retrieved_document)

        return search_result
    
    def get_document(self, document_query: DocumentQuery, context):
        # use associated sparse_searcher to retrieve the results
        return self.sparse_searcher.get_document(document_query, context)
