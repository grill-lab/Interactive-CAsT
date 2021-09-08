from .abstract_trecweb_converter import AbstractTrecwebConverter
from typing import Tuple, Dict

class MarcoTrecwebConverter(AbstractTrecwebConverter):

    
    def get_document_attributes(self, document) -> Tuple[str, str, str, str]:

        try:
            idx, url, title, body = document.strip().split('\t')
            return idx, url, title, body
        except ValueError:
            #print("Either the id, url, title or body is missing")
            return None
    
    def create_duplicates_dictionary(self, duplicates_file_path) -> Dict:

        duplicates_lookup_dict = {}

        with open(duplicates_file_path) as duplicates_file:
            for line in duplicates_file:
                
                document_ids = line.strip().split(':')
                if len(document_ids[1]) > 0:
                    duplicate_ids = document_ids[-1].split(',')
                    for doc_id in duplicate_ids:
                        duplicates_lookup_dict[doc_id] = 1
        
        print("There are {} duplicates".format(len(duplicates_lookup_dict)))
        return duplicates_lookup_dict