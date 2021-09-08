from .abstract_passage_chunker import AbstractPassageChunker
from typing import Dict, List

import spacy

nlp = spacy.load("en_core_web_sm", exclude=["parser", "tagger", "ner", "attribute_ruler", "lemmatizer", "tok2vec"])
nlp.enable_pipe("senter")
nlp.max_length = 1500000 #for documents that are longer than the spacy character limit


class SpacyPassageChunker(AbstractPassageChunker):

    def __init__(self, max_passage_size) -> None:
        super().__init__(max_passage_size)

    
    def tokenize_document(self, document_body) -> None:
        spacy_document = nlp(document_body)
        self.document_sentences = list(spacy_document.sents)

    
    def chunk_document(self, passage_size = 250) -> List[Dict]:

        passages = []
        sentence_count = len(self.document_sentences)
        sentences_word_count = [len([token for token in sentence]) for sentence in self.document_sentences]
        
        current_idx = 0
        current_passage_word_count = 0
        current_passage = ''
        sub_id = 0
        
        for i in range(sentence_count):

            #0.67 is used to control passages that may overflow the max passage size
            if current_passage_word_count >= (self.max_passage_size * 0.67):
                passages.append({
                    "body": current_passage,
                    "id": sub_id
                })

                #reset the current passage to an empty string
                current_passage = ''
                current_passage_word_count = 0
                
                current_idx = i
                sub_id += 1
            
            current_passage += self.document_sentences[i].text + ' '
            current_passage_word_count += sentences_word_count[i]

        #append the remaining sentences, if any, to a passage
        current_passage = ' '.join(sentence.text for sentence in self.document_sentences[current_idx:])
        passages.append({
            "body": current_passage,
            "id": sub_id
        })
        
        return passages
    
