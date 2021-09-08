from .abstract_trecweb_converter import AbstractTrecwebConverter
from typing import Tuple, Dict
import json


class WapoTrecwebConverter(AbstractTrecwebConverter):
    

    def get_document_attributes(self, document) -> Tuple[str, str, str, str]:

        document = json.loads(document)
        
        idx = 'WAPO_' + str(document['id'])
        
        #Get the document url
        url = '/#'
        if document["article_url"]:
            if "www.washingtonpost.com" not in document["article_url"]:
                url = "https://www.washingtonpost.com" + document['article_url']
            else:
                url = document['article_url']
        
        #Get the document title
        title = ''
        if document['title'] != None:
            title = document['title'].replace("\n", " ")

        
        #Get the document body
        body = ''
        contents = document['contents']
        try:
            for item in contents:
                if 'subtype' in item and item['subtype'] == 'paragraph':
                    body += ' ' + item['content']
        except:
            body += 'No body'
        
        
        return idx, url, title, body
    

    def create_duplicates_dictionary(self, duplicates_file_path) -> Dict:
        
        duplicates_lookup_dict = {}

        with open(duplicates_file_path) as duplicates_file:
            for line in duplicates_file:
                document_ids = line.strip().split(' ')

                if document_ids[0] == document_ids[1]:
                    #the duplicate has the same id as the original
                    duplicates_lookup_dict[document_ids[1]] = 2
                else:
                    #the duplicate has the same id as the original
                    duplicates_lookup_dict[document_ids[1]] = 1

        
        return duplicates_lookup_dict
