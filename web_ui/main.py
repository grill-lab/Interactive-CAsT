# from flask import Flask, render_template, request
import os

import time
import json
import logging
import sys
import grpc

from tqdm import tqdm
sys.path.insert(0, '/shared')
sys.path.insert(0, '/shared/compiled_protobufs')


from search_result_pb2 import SearchResult
from searcher_pb2 import SearchQuery, DocumentQuery
from searcher_pb2_grpc import SearcherStub

from reranker_pb2 import RerankRequest
from reranker_pb2_grpc import RerankerStub

# from rewriter_pb2 import RewriteRequest
# from rewriter_pb2_grpc import RewriterStub

from summariser_pb2 import SummaryRequest
from summariser_pb2_grpc import SummariserStub

from utils.conversion_utils import context_converter
from google.protobuf.json_format import MessageToDict


searcher_channel = grpc.insecure_channel(os.environ['SEARCHER_URL'])
search_client = SearcherStub(searcher_channel)

reranker_channel = grpc.insecure_channel(os.environ['RERANKER_URL'])
rerank_client = RerankerStub(reranker_channel)

# rewriter_channel = grpc.insecure_channel(os.environ['REWRITER_URL'])
# rewrite_client = RewriterStub(rewriter_channel)

summariser_channel = grpc.insecure_channel(os.environ['SUMMARISER_URL'])
summariser_client = SummariserStub(summariser_channel)

topics_file = "/shared/data/2022_evaluation_topics_flattened_duplicated_v1.0.json"
field = 'manual_rewritten_utterance'
run_name = "BM25_T5_BART"
run_type = "manual"

with open(topics_file) as f:
    topics = json.load(f)

# seen topics
seen_topics = set()

# initialise run dict
run_dict = {
    "run_name" : run_name,
    "run_type" : run_type,
    "turns": []
}

search_query = SearchQuery()
search_query.num_hits = 100
search_query.search_parameters.parameters["b"] = "0.82"
search_query.search_parameters.parameters["k1"] = "4.46"

for topic in tqdm(topics):
    for turn in topic['turn']:
        global_turn_number = f"{topic['number']}_{turn['number']}"
        if global_turn_number in seen_topics:
            continue
        else:
            response_dict = {
                "turn_id" : global_turn_number,
                "responses" : []
            }
            # search
            search_query.query = turn[field]
            search_result = search_client.search(search_query)
            print(f"Search completed for {global_turn_number}")

            # rerank
            rerank_request = RerankRequest()
            rerank_request.search_query = search_query.query


            rerank_request.num_passages = 1000
            rerank_request.search_result.MergeFrom(search_result)
            rerank_result = rerank_client.rerank(rerank_request)
            print(f"Ranking completed for {global_turn_number}")

            # summarise
            summary_request = SummaryRequest()
            summary_request.rerank_result.MergeFrom(rerank_result)
            summary_request.num_passages = 3
            summary_result = summariser_client.summarise(summary_request)
            print(f"Summary generated for {global_turn_number}")

            # demo only has one response
            response_dict['responses'].append({
                "text" : summary_result.summary,
                "rank" : 1,
                "provenance" : [
                    {
                        "id" : passage.id,
                        "text": passage.body,
                        "score": passage.score
                    }
                    for passage in rerank_result.passages
                ]
            })

            run_dict['turns'].append(response_dict)
            seen_topics.add(global_turn_number)

with open(f"/shared/data/{run_name}_{run_type}.json", "w") as sample_run_file:
    json.dump(run_dict, sample_run_file, indent=4, ensure_ascii=False)