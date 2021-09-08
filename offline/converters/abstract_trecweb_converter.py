from abc import ABC, abstractmethod
from typing import Dict, Tuple


class AbstractTrecwebConverter(ABC):

    @abstractmethod
    def get_document_attributes(self, document) -> Tuple[str, str, str, str]:
        """
        Retrieves the id, url, title and body of a document
        """
        
        pass

    @abstractmethod
    def create_duplicates_dictionary(self, duplicates_file_path) -> Dict:
        """
        Creates a dictionary, from the duplicates file, to easily check 
        if a document is a duplicate
        """

        pass