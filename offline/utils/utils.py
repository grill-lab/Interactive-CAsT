from typing import Dict, List
from tqdm import tqdm

def add_passage_ids(passages: List) -> str:

    """
    Reforms the document body to include it's passage splits
    """

    passage_splits = ''

    for passage in passages:
        passage_splits += '<PASSAGE id={}>\n'.format(passage["id"])
        passage_splits += passage["body"] + '\n'
        passage_splits += '</PASSAGE>\n'

    
    return passage_splits

def create_trecweb_entry(idx: str, url: str, title: str, body: str) -> str:
    
    """
    Creates a trecweb entry for a document
    """

    content = '<DOC>\n'
    content += '<DOCNO>'
    content += idx
    content += '</DOCNO>\n'
    content += '<DOCHDR>\n'
    content += '</DOCHDR>\n'
    content += '<HTML>\n'
    content += '<TITLE>'
    content += title
    content += '</TITLE>\n'
    content += '<URL>'
    content += url
    content += '</URL>\n'
    content += '<BODY>\n'
    content += body
    content += '</BODY>\n'
    content += '</HTML>\n'
    content += '</DOC>\n'
    content += '\n'
    
    return content

def write_documents_to_file(collection_path: str, collection_name : str, converter, passage_chunker, document_count: int, duplicates_file_path: str = None, num_documents = None):

    """
    Single interface to write documents to the final trecweb file.
    """

    count = 0

    duplicates_lookup_dict = None
    if duplicates_file_path:
        duplicates_lookup_dict = converter.create_duplicates_dictionary(duplicates_file_path)

    with open(collection_path, 'r') as collection:
        with open('./data/processed_trecweb/' + collection_name + ".trecweb", 'a') as trecweb_file:
            for document in tqdm(collection, total=document_count):

                if not converter.get_document_attributes(document):
                    #skipping because we do not have all the fields for this doc, see Marco converter
                    continue

                doc_id, doc_url, doc_title, doc_body = converter.get_document_attributes(document)

                if duplicates_lookup_dict and collection_name == 'marco':
                    if doc_id in duplicates_lookup_dict:
                        #print("{} is a duplicate in the Marco collection!".format(doc_id))
                        continue
                
                if duplicates_lookup_dict and collection_name == 'wapo':

                    if duplicates_lookup_dict.get(doc_id) == 1:
                        #print("{} is a duplicate in the WaPo collection!".format(doc_id))
                        continue

                    if duplicates_lookup_dict.get(doc_id) == 2:
                        #print("Processed the first copy of {} in the WaPo collection!".format(doc_id))
                        duplicates_lookup_dict[doc_id] = 1
                
                passage_chunker.tokenize_document(doc_body)
                passages = passage_chunker.chunk_document()
                passage_splits = add_passage_ids(passages)
                trecweb_entry = create_trecweb_entry(doc_id, doc_url, doc_title, passage_splits)
                trecweb_file.write(trecweb_entry)

                
                if num_documents:
                    # process only the user specified number of documents
                    count += 1
                    if count >= num_documents:
                        break