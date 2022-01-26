from .abstract_searcher import AbstractSearcher
from .sparse_searcher import SparseSearcher
from .dense_searcher import DenseSearcher
from .hybrid_searcher import SparseDenseSearcher

class SearcherSelector(AbstractSearcher):

    def __init__(self) -> None:
        self.searchers = {
            "SPARSE" : SparseSearcher(),
            "DENSE" : DenseSearcher(),
            "HYBRID" : SparseDenseSearcher()
        }

        self.chosen_searcher = None
    
    def search(self, search_query, context):
        
        if search_query.searcher_type == 0:
            self.chosen_searcher = self.searchers["SPARSE"]
        elif search_query.searcher_type == 1:
            self.chosen_searcher = self.searchers["DENSE"]
        elif search_query.searcher_type == 2:
            self.chosen_searcher = self.searchers["HYBRID"]
        
        return self.chosen_searcher.search(search_query, context)
    
    def get_document(self, document_request, context):
        # user might want to look up a doc directly without performing a
        # search first

        if self.chosen_searcher:
            return self.chosen_searcher.get_document(document_request, context)
        
        # only a sparse searcher can do document lookups, so we default to it
        else:
            if document_request.searcher_type == 0:
                self.chosen_searcher = self.searchers["SPARSE"]
            
            return self.chosen_searcher.get_document(document_request, context)
        
        