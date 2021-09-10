from .abstract_searcher import AbstractSearcher
from .pyserini_searcher import PyseriniSearcher

class BackendSelector(AbstractSearcher):

    def __init__(self) -> None:
        self.searchers = {
            "PYSERINI" : PyseriniSearcher()
        }

        self.chosen_backend = None
    
    def search(self, search_query, context):
        
        if search_query.search_backend == 0:
            self.chosen_backend = self.searchers["PYSERINI"]
        
        return self.chosen_backend.search(search_query, context)
    
    def get_document(self, document_request, context):
        # user might want to look up a doc directly without performing a
        # search first

        if self.chosen_backend:
            return self.chosen_backend.get_document(document_request, context)
        
        else:
            if document_request.search_backend == 0:
                self.chosen_backend = self.searchers["PYSERINI"]
            
            return self.chosen_backend.get_document(document_request, context)
        
        