from .abstract_searcher import AbstractSearcher
from pyserini.search.lucene import LuceneSearcher
from searcher_pb2 import SearchQuery, DocumentQuery
from search_result_pb2 import SearchResult, Document, Passage
from utils.passage_chunkers import PassageChunker

import json
import logging

class SparseSearcher(AbstractSearcher):

    def __init__(self):

        self.indexes = {
            'ALL' : LuceneSearcher('../../shared/indexes/sparse/sparse_test'),
            # 'KILT' : SimpleSearcher('../../shared/indexes/kilt'),
            # 'MARCO' : SimpleSearcher('../../shared/indexes/marco'),
            # 'WAPO' : SimpleSearcher('../../shared/indexes/wapo')
            # new indices go here
        }

        self.chosen_index = None
        self.passage_chunker = PassageChunker()
    
    def search(self, search_query: SearchQuery, context):

        query: str = search_query.query
        num_hits: int = search_query.num_hits

        logging.info("WE ARE USING THE SPARSE SEARCHER")

        if search_query.search_parameters.collection == 0:
            self.chosen_index = self.indexes['ALL']
        
        # if search_query.search_parameters.collection == 1:
        #     self.chosen_searcher = self.indexes['KILT']
        
        # if search_query.search_parameters.collection == 2:
        #     self.chosen_searcher = self.indexes['MARCO']
        
        # if search_query.search_parameters.collection == 3:
        #     self.chosen_searcher = self.indexes['WAPO']
        
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

        document_id = document_query.document_id
        
        # index = document_id.split("_")[0].strip()
        self.chosen_index = self.indexes["ALL"] # ensure its the default

        hit = self.chosen_index.doc(document_id)
        retrieved_document = self.__convert_search_response(hit)

        return retrieved_document

    def __convert_search_response(self, hit):

        retrieved_document = Document()
        
        try:
            # if hit is a document from regular search
            raw_document = json.loads(hit.raw)
            retrieved_document.id = hit.docid
            retrieved_document.score = hit.score
        except:
            # if hit is a document lookup request
            # There's no score in this case
            raw_document = json.loads(hit.raw())
            retrieved_document.id = hit.docid()
        
        retrieved_document.title = raw_document['title']
        retrieved_document.url = raw_document['url']

        self.passage_chunker.tokenize_document(raw_document["text"])
        passages = self.passage_chunker.chunk_document()

        for passage in passages:
            chunked_passage = Passage()
            chunked_passage.id = str(passage["id"])
            chunked_passage.body = passage["body"]
            retrieved_document.passages.append(chunked_passage)
        
        return retrieved_document
    