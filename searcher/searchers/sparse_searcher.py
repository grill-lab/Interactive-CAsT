from concurrent.futures import process
from .abstract_searcher import AbstractSearcher
from pyserini.search.lucene import LuceneSearcher
from searcher_pb2 import SearchQuery, DocumentQuery
from search_result_pb2 import SearchResult, Document, Passage

import json
import logging
import re

from bs4 import BeautifulSoup as bs
import lxml

class SparseSearcher(AbstractSearcher):

    def __init__(self):

        self.indexes = {
            'ALL' : LuceneSearcher('/index')
            # new indices go here
        }

        self.chosen_index = None
    
    def search(self, search_query: SearchQuery, context):

        query: str = search_query.query
        num_hits: int = search_query.num_hits

        logging.info("WE ARE USING THE SPARSE SEARCHER")

        if search_query.search_parameters.collection == 0:
            self.chosen_index = self.indexes['ALL']
        
        bm25_b = search_query.search_parameters.parameters["b"]
        bm25_k1 = search_query.search_parameters.parameters["k1"]

        
        self.chosen_index.set_bm25(float(bm25_k1), float(bm25_b))
        hits = self.chosen_index.search(query, num_hits)

        search_result = SearchResult()

        for hit in hits:
            retrieved_document = self.__convert_search_response(hit)
            search_result.documents.append(retrieved_document)

        return search_result

    
    def get_document(self, document_query: DocumentQuery, context):
        pass

    def __convert_search_response(self, hit):

        retrieved_document = Document()

        retrieved_document.id = hit.docid
        retrieved_document.score = hit.score
        processed_document = bs(hit.raw, "lxml")
        extracted_passages = processed_document.find_all("passage")
        extracted_passages = [
            {
                'id': f"{hit.docid}-{passage['id']}", 
                "body": passage.text
            } 
            
            for passage in extracted_passages
        ]

        for passage in extracted_passages:
            chunked_passage = Passage()
            chunked_passage.id = str(passage["id"])
            chunked_passage.body = passage["body"]
            retrieved_document.passages.append(chunked_passage)
        
        return retrieved_document
    
