from .abstract_trecweb_converter import AbstractTrecwebConverter
from typing import Tuple, Dict
import json


class KILTTrecwebConverter(AbstractTrecwebConverter):

    
    def get_document_attributes(self, document) -> Tuple[str, str, str, str]:
        
        parsed_document = json.loads(document)
        idx = 'KILT_' + parsed_document['wikipedia_id']
        url = parsed_document['history']['url']
        title = parsed_document['wikipedia_title']
        body = ' '.join(parsed_document['text'])        

        return idx, url, title, body

    
    def create_duplicates_dictionary(self, duplicates_file_path) -> Dict:
        return super().create_duplicates_dictionary(duplicates_file_path)
    