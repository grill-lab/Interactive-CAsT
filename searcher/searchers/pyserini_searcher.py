from .abstract_searcher import AbstractSearcher
from pyserini.search import SimpleSearcher
from searcher_pb2 import SearchQuery, DocumentQuery
from search_result_pb2 import SearchResult, Document, Passage

from bs4 import BeautifulSoup as bs
import lxml

class PyseriniSearcher(AbstractSearcher):

    def __init__(self):

        self.indexes = {
            'ALL' : SimpleSearcher('../../shared/indexes/all'),
            'KILT' : SimpleSearcher('../../shared/indexes/kilt'),
            'MARCO' : SimpleSearcher('../../shared/indexes/marco'),
            'WAPO' : SimpleSearcher('../../shared/indexes/wapo')
            #new indices go here
        }

        self.chosen_searcher = None
    
    def search(self, search_query: SearchQuery, context):


        query: str = search_query.query
        num_hits: int = search_query.num_hits

        if search_query.search_parameters.collection == 0:
            self.chosen_searcher = self.indexes['ALL']
        
        if search_query.search_parameters.collection == 1:
            self.chosen_searcher = self.indexes['KILT']
        
        if search_query.search_parameters.collection == 2:
            self.chosen_searcher = self.indexes['MARCO']
        
        if search_query.search_parameters.collection == 3:
            self.chosen_searcher = self.indexes['WAPO']
        
        hits = self.chosen_searcher.search(query, num_hits)

        search_result = SearchResult()

        for hit in hits:
            retrieved_document = self.__convert_search_response(hit)
            search_result.documents.append(retrieved_document)

        return search_result

    
    def get_document(self, document_query: DocumentQuery, context):

        document_id = document_query.document_id
        
        index = document_id.split("_")[0].strip()

        self.chosen_searcher = self.indexes[index]

        hit = self.chosen_searcher.doc(document_id)


        retrieved_document = self.__convert_search_response(hit)

        return retrieved_document

    
    def __convert_search_response(self, hit):

        retrieved_document = Document()
        soup = None

        try:
            #This works if it is a regular search hit
            soup = bs(hit.raw, "lxml")
            retrieved_document.id = hit.docid
            retrieved_document.score = hit.score
        except:
            #This works if it is a document lookup
            soup = bs(hit.raw(), "lxml")
            retrieved_document.id = hit.docid()
        
        retrieved_document.url = soup.find("url").text
        retrieved_document.title = soup.find("title").text
        
        
        passages = soup.find_all("passage")
        
        for passage in passages:
            chunked_passage = Passage()
            chunked_passage.id = passage["id"]
            chunked_passage.body = passage.text

            retrieved_document.passages.append(chunked_passage)    
        
        return retrieved_document
    
