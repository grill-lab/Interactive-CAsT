from .abstract_passage_chunker import AbstractPassageChunker
from typing import Dict, List

import spacy

nlp = spacy.load("en_core_web_sm", exclude=["parser", "tagger", "ner", "attribute_ruler", "lemmatizer", "tok2vec"])
nlp.enable_pipe("senter")
nlp.max_length = 1500000 #for documents that are longer than the spacy character limit


class SpacyPassageChunker(AbstractPassageChunker):

    def __init__(self) -> None:
        super().__init__()

    
    def tokenize_document(self, document_body) -> None:
        spacy_document = nlp(document_body)
        self.document_sentences = list(spacy_document.sents)
        self.sentences_word_count = [
            len([token for token in sentence]) 
            for sentence in self.document_sentences
        ]