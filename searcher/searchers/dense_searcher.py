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
            'DOCUMENTS' : SimpleDenseSearcher('../../shared/indexes/dense/dense_doc_index', 
                            'castorini/ance-msmarco-passage'),
            # 'ENTITIES' : SimpleDenseSearcher('../../shared/indexes/dense/dense_entity_index', 
            #                 'castorini/ance-msmarco-passage')
            # new indices go here
        }

        self.chosen_index = None
        self.sparse_searcher = SparseSearcher()
    
    def search(self, search_query: SearchQuery, context):

        query: str = search_query.query
        num_hits: int = search_query.num_hits

        print("WE ARE USING THE DENSE SEARCHER")

        # we need a corresponing sparse searcher to retrieve doc attributes
        if search_query.search_parameters.collection == 0:
            self.chosen_index = self.indexes['DOCUMENTS']
            self.sparse_searcher.chosen_index = self.sparse_searcher.indexes['DOCUMENTS']
        elif search_query.search_parameters.collection == 4:
            self.chosen_index = self.indexes['ENTITIES']
            self.sparse_searcher.chosen_index = self.sparse_searcher.indexes['ENTITIES']
        
        hits = self.chosen_index.search(query, num_hits)
        search_result = SearchResult()

        document_query = DocumentQuery()
        document_query.searcher_type = 0

        for hit in hits:
            try:
                document_query.document_id = hit.docid
                retrieved_document = self.get_document(document_query, context)
                search_result.documents.append(retrieved_document)
            except:
                 print(f"Doc with id {hid.docid} has a missing field")

        return search_result
    
    def get_document(self, document_query: DocumentQuery, context):
        # use associated sparse_searcher to retrieve the results
        return self.sparse_searcher.get_document(document_query, context)
