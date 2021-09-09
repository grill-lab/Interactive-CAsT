import argparse
import os
import subprocess

from converters import KILTTrecwebConverter, MarcoTrecwebConverter, WapoTrecwebConverter
from passage_chunkers import SpacyPassageChunker
from index_generator import PyseriniIndexGenerator
from utils.utils import write_documents_to_file

parser = argparse.ArgumentParser(description='Offline Pipeline Parameters')
parser.add_argument('--kilt_collection', type=str, default="./data/collections/kilt_knowledgesource.json", help="Path to the raw kilt collection")

parser.add_argument('--marco_collection', type=str, default="./data/collections/msmarco-docs.tsv", help="Path to the raw marco collection")
parser.add_argument('--marco_duplicates', type=str, default="./data/duplicates_files/marco_duplicates.txt", help="Path to marco duplicates files")

parser.add_argument('--wapo_collection', type=str, default="./data/collections/TREC_Washington_Post_collection.v4.jl", help="Path to the raw wapo collection")
parser.add_argument('--wapo_duplicates', type=str, default="./data/duplicates_files/wapo-near-duplicates", help="Path to wapo duplicates files")

parser.add_argument('--passage_chunker', type=str, default="spacy", help="Passage Chunker, spacy or regex")
parser.add_argument('--max_passage_size', type=int, default=250, help="Max passage size: int")

parser.add_argument('--document_count', type=int, default=None, help="Number of documents to process per collection")

parser.add_argument('--skip_process_all', default=False, action='store_true')
parser.add_argument('--skip_process_kilt', default=False, action='store_true')
parser.add_argument('--skip_process_marco', default=False, action='store_true')
parser.add_argument('--skip_process_wapo', default=False, action='store_true')

parser.add_argument('--skip_indexing', default=False, action='store_true')

parser.add_argument('--indexer_input_dir', type=str, default="./data/index_candidates", help="Directory with processed files for indexing")
parser.add_argument('--indexer_output_dir', type=str, default="../shared/indexes", help="Directory to write indexes to")

if __name__ == '__main__':

    args = parser.parse_args()
    
    passage_chunker = None
    if args.passage_chunker == 'spacy':
        passage_chunker = SpacyPassageChunker(max_passage_size=args.max_passage_size)

    
    index_generator = PyseriniIndexGenerator()

    
    trecweb_dump_path = './data/processed_trecweb'

    if not os.path.isdir(trecweb_dump_path):
        os.mkdir(trecweb_dump_path)
    
    if not os.path.isdir(args.indexer_input_dir):
        os.mkdir(args.indexer_input_dir)


    if not args.skip_process_kilt:
        print("Processing KILT...")
        kilt_trecweb_converter: KILTTrecwebConverter = KILTTrecwebConverter()
        write_documents_to_file(args.kilt_collection, 'kilt', kilt_trecweb_converter, passage_chunker, 5903530, num_documents=args.document_count)

        if not args.skip_indexing:
            print("Indexing the KILT trecweb file..")
            subprocess.run(["cp", trecweb_dump_path + "/kilt.trecweb", args.indexer_input_dir])
            index_generator.generate_index(args.indexer_input_dir, args.indexer_output_dir + "/kilt")
            subprocess.run(["rm", args.indexer_input_dir + "/kilt.trecweb"])
    
    if not args.skip_process_marco:
        print("Processing MARCO...")
        marco_trecweb_converter: MarcoTrecwebConverter = MarcoTrecwebConverter()
        write_documents_to_file(args.marco_collection, 'marco', marco_trecweb_converter, passage_chunker, 3213835, args.marco_duplicates, num_documents=args.document_count)

        if not args.skip_indexing:
            print("Indexing the MARCO trecweb file..")
            subprocess.run(["cp", trecweb_dump_path + "/marco.trecweb", args.indexer_input_dir])
            index_generator.generate_index(args.indexer_input_dir, args.indexer_output_dir + "/marco")
            subprocess.run(["rm", args.indexer_input_dir + "/marco.trecweb"])
    
    if not args.skip_process_wapo:
        print("Processing WaPo..")
        wapo_trecweb_converter: WapoTrecwebConverter = WapoTrecwebConverter()
        write_documents_to_file(args.wapo_collection, 'wapo', wapo_trecweb_converter, passage_chunker, 728626, args.wapo_duplicates, num_documents=args.document_count)

        if not args.skip_indexing:
            print("Indexing the WaPo trecweb file..")
            subprocess.run(["cp", trecweb_dump_path + "/wapo.trecweb", args.indexer_input_dir])
            index_generator.generate_index(args.indexer_input_dir, args.indexer_output_dir + "/wapo")
            subprocess.run(["rm", args.indexer_input_dir + "/wapo.trecweb"])
    
    if not args.skip_process_all:
        #check if kilt has been processed, if not process it.
        if not os.path.isfile("./data/processed_trecweb/kilt.trecweb"):
            print("Processing KILT...")
            kilt_trecweb_converter: KILTTrecwebConverter = KILTTrecwebConverter()
            write_documents_to_file(args.kilt_collection, 'kilt', kilt_trecweb_converter, passage_chunker, 5903530, num_documents=args.document_count)
        
        #check if marco has been processed, if not process it.
        if not os.path.isfile("./data/processed_trecweb/marco.trecweb"):
            print("Processing Marco...")
            marco_trecweb_converter: MarcoTrecwebConverter = MarcoTrecwebConverter()
            write_documents_to_file(args.marco_collection, 'marco', marco_trecweb_converter, passage_chunker, 3213835, args.marco_duplicates, num_documents=args.document_count)
        
        #check if wapo has been processed, if not, process it
        if not os.path.isfile("./data/processed_trecweb/wapo.trecweb"):
            print("Processing WaPo...")
            wapo_trecweb_converter: MarcoTrecwebConverter = MarcoTrecwebConverter()
            write_documents_to_file(args.wapo_collection, 'marco', wapo_trecweb_converter, passage_chunker, 3213835, args.wapo_duplicates, num_documents=args.document_count)

        
        #no need to copy over files since directory has all we need
        if not args.skip_indexing:
            print("Indexing the entire collection...")
            index_generator.generate_index(trecweb_dump_path, args.indexer_output_dir + "/all")  




        





