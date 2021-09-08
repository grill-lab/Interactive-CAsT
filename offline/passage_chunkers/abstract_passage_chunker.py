from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractPassageChunker(ABC):

    @abstractmethod
    def __init__(self, max_passage_size) -> None:
        self.document_sentences = None
        self.max_passage_size = max_passage_size
    
    def tokenize_document(self, document_body) -> None:
        """
        Tokenizes the document into sentences
        """
        pass

    def chunk_document(self) -> List[Dict]:
        """
        Creates the passage chunks for a given document
        """
        pass


