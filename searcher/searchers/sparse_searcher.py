from .abstract_searcher import AbstractSearcher
from pyserini.search import SimpleSearcher
from searcher_pb2 import SearchQuery, DocumentQuery
from search_result_pb2 import SearchResult, Document, Passage

import json
import logging

class SparseSearcher(AbstractSearcher):

    def __init__(self):

        self.indexes = {
            'DOCUMENTS' : SimpleSearcher('../../shared/indexes/sparse/sparse_doc_index'),
            'ENTITIES' : SimpleSearcher('../../shared/indexes/sparse/sparse_entity_index'),
        }

        self.chosen_index = None
    
    def search(self, search_query: SearchQuery, context):

        query: str = search_query.query
        num_hits: int = search_query.num_hits

        print("WE ARE USING THE SPARSE SEARCHER")

        if search_query.search_parameters.collection == 0:
            self.chosen_index = self.indexes['DOCUMENTS']
        elif search_query.search_parameters.collection == 4:
            self.chosen_index = self.indexes['ENTITIES']
        
        if search_query.search_parameters.parameters["set_rm3"] == "True":
            self.chosen_index.set_rm3()
        else:
            self.chosen_index.unset_rm3()
        
        print(f"SPARSE Searcher is using RM3: {self.chosen_index.is_using_rm3()}")
        
        bm25_b = search_query.search_parameters.parameters["b"]
        bm25_k1 = search_query.search_parameters.parameters["k1"]
        
        self.chosen_index.set_bm25(float(bm25_k1), float(bm25_b))
        hits = self.chosen_index.search(query, num_hits)

        search_result = SearchResult()

        for hit in hits:
            try:
                retrieved_document = self.__convert_search_response(hit)
                search_result.documents.append(retrieved_document)
            except:
                print(f"Doc with id {hid.docid} has a missing field")

        return search_result

    
    def get_document(self, document_query: DocumentQuery, context):

        document_id = document_query.document_id
        
        # index = document_id.split("_")[0].strip()
        if document_query.collection == 0:
            self.chosen_index = self.indexes['DOCUMENTS']
        elif document_query.collection == 4:
            self.chosen_index = self.indexes['ENTITIES']

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

        if not raw_document.get("wikipedia_title"):
            retrieved_document.title = raw_document.get("title")
            retrieved_document.url = raw_document.get("url")
        else:
            retrieved_document.title = raw_document.get("wikipedia_title")
            wiki_title = retrieved_document.title.replace(" ", "_")
            retrieved_document.url = raw_document.get("url", f"https://en.wikipedia.org/wiki/{wiki_title}")
        
        # check if we have a passage field
        if not raw_document.get("passage"):
            # just one passage
            chunked_passage = Passage()
            chunked_passage.body = raw_document["html_contents"]
            chunked_passage.id = "1" # there's just one passage
            retrieved_document.passages.append(chunked_passage)
        else:
            # passage delineated index
            for idx, passage in enumerate(raw_document["passage"]):
                chunked_passage = Passage()
                chunked_passage.id = f"{idx + 1}"
                chunked_passage.body = passage
                retrieved_document.passages.append(chunked_passage) 
        
        return retrieved_document
    
