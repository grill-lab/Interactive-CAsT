from .abstract_reranker import AbstractReranker
from .pygaggle import MonoT5, MonoBERT, Query, Text
from search_result_pb2 import SearchResult, Document, Passage
from reranker_pb2 import RerankRequest

class PygaggleReranker(AbstractReranker):

    def __init__(self):

        self.rerankers = {
            'T5' : MonoT5(),
            'BERT' : MonoBERT()
        }

        self.chosen_reranker = None

    def rerank(self, rerank_request: RerankRequest, context):

        if rerank_request.reranker == 0:
            self.chosen_reranker = self.rerankers['T5']
        
        if rerank_request.reranker == 1:
            self.chosen_reranker = self.rerankers['BERT']
        
        first_pass_search_result: SearchResult = rerank_request.search_result

        num_passages_to_rerank = rerank_request.num_passages

        search_result = SearchResult()

        parsed_passages, lookup_dictionary = self.__create_reranker_input(
            first_pass_search_result, num_passages_to_rerank
        )

        texts = [ Text(passage[1], {'id': passage[0]}, 0) for passage in parsed_passages]

        query = Query(rerank_request.search_query)

        reranked_passages = self.chosen_reranker.rerank(query, texts)

        reordered_documents = self.__collect_passages(reranked_passages, lookup_dictionary)

        for document in reordered_documents:
            proto_document = Document()

            for passage in document["passages"]:
                proto_passage = Passage()
                proto_passage.id = passage["passage_id"]
                proto_passage.body = passage["body"]
                proto_passage.score = passage["score"]

                proto_document.passages.append(proto_passage)
            
            proto_document.id = document["id"]
            proto_document.title = document["title"]
            proto_document.url = document["url"]
            
            search_result.documents.append(proto_document)

        return search_result


    def __create_reranker_input(self, search_result, num_passages_to_rerank):

        parsed_passages = []
        lookup_dictionary = {}

        for document in search_result.documents:
            for passage in document.passages[:num_passages_to_rerank]:

                passage_list = []
                passage_list.append("{}:{}".format(document.id, passage.id))
                passage_list.append(passage.body)

                if not lookup_dictionary.get(document.id):
                    
                    lookup_dictionary[document.id] = {
                        'title': document.title,
                        'url' : document.url
                    }

                parsed_passages.append(passage_list)
        
        return parsed_passages, lookup_dictionary
    
    def __collect_passages(self, reranker_output, lookup_dictionary):

        # desired format -> {'id': doc_id, 'title': title, 'url': url, 'passages': []}
        # passage in passages are of the form {'score': score, 'id': 'passage_id', 'body': body}

        ordered_documents = []
        unique_documents = {}

        for passage in reranker_output:

            document_id = passage.metadata['id'].split(':')[0]
            passage_id = passage.metadata['id'].split(':')[1]

            # check if we have seen the document before
            if document_id not in unique_documents:

                unique_documents[document_id] = {'count': 1, 'idx': len(ordered_documents)}

                document_object = {
                    'id' : document_id,
                    'title' : lookup_dictionary[document_id]['title'],
                    'url' : lookup_dictionary[document_id]['url'],
                    'passages' : []
                }

                document_object['passages'].append({
                    "passage_id" : passage_id,
                    "score" : passage.score,
                    "body" : passage.text
                })

                ordered_documents.append(document_object)
            
            else:
                #get the index of the document
                idx = unique_documents[document_id]['idx']

                ordered_documents[idx]['passages'].append({
                    "passage_id" : passage_id,
                    "score" : passage.score,
                    "body" : passage.text
                })
        
        
        return ordered_documents








