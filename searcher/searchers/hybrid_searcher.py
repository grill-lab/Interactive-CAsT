from pyserini.hsearch import HybridSearcher
from .sparse_searcher import SparseSearcher
from .dense_searcher import DenseSearcher
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher
from .abstract_searcher import AbstractSearcher

from searcher_pb2 import SearchQuery, DocumentQuery
from search_result_pb2 import SearchResult, Document, Passage
import logging

class SparseDenseSearcher(DenseSearcher, AbstractSearcher):

    def __init__(self):

        DenseSearcher.__init__(self)

        self.indexes = {
            'DOCUMENTS' : HybridSearcher(
                SimpleDenseSearcher('../../shared/indexes/dense/dense_doc_index', 
                            'castorini/ance-msmarco-passage'),
                SimpleSearcher('../../shared/indexes/sparse/sparse_doc_index')
            ),
            # 'ENTITIES' : HybridSearcher(
            #     SimpleDenseSearcher('../../shared/indexes/dense/dense_entity_index', 
            #                 'castorini/ance-msmarco-passage'),
            #     SimpleSearcher('../../shared/indexes/sparse/sparse_entity_index')
            # ),
        }
    
    def search(self, search_query: SearchQuery, context):

        query: str = search_query.query
        num_hits: int = search_query.num_hits

        print("WE ARE USING THE HYBRID SEARCHER")
        
        # we need a corresponing sparse searcher to retrieve doc attributes
        if search_query.search_parameters.collection == 0:
            self.chosen_index = self.indexes['DOCUMENTS']
            self.sparse_searcher.chosen_index = self.sparse_searcher.indexes['DOCUMENTS']
        elif search_query.search_parameters.collection == 4:
            self.chosen_index = self.indexes['ENTITIES']
            self.sparse_searcher.chosen_index = self.sparse_searcher.indexes['ENTITIES']
        
        hits = self.chosen_index.search(query, num_hits, num_hits)
        search_result = SearchResult()

        document_query = DocumentQuery()
        document_query.searcher_type = 0

        for hit in hits:
            try:
                document_query.document_id = hit.docid

                retrieved_document = self.get_document(document_query, context)
                search_result.documents.append(retrieved_document)
            except:
                continue

        return search_result