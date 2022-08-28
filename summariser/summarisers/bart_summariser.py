from .abstract_summariser import AbstractSummariser
from summariser_pb2 import SummaryRequest, SummaryResult

from transformers import pipeline
import torch
import os


class BARTSummariser(AbstractSummariser):
    def __init__(self) -> None:
        summariser_cache_directory = "/shared/models/bart_summariser"
        summariser_model_name: str = "facebook/bart-large-cnn"

        self.summarisers = {
            "BART": pipeline(
                "summarization", model=summariser_model_name, 
                model_kwargs = {"cache_dir": summariser_cache_directory},
                device = -1 if not torch.cuda.is_available() else 0
            )
        }

        self.summariser = None

    def summarise(self, summary_request, context):

        summary_result = SummaryResult()
        if summary_request.summariser == 0:
            self.summariser = self.summarisers['BART']
        
        num_passages = summary_request.num_passages
        top_n_passages = '\n'.join([passage.body for passage in summary_request.rerank_result.passages[:num_passages]])
        output = self.summariser(
            top_n_passages, 
            max_length=200, 
            min_length=30, 
            do_sample=False,
            truncation=True
        )

        summary_result.summary = output[0]['summary_text']

        return summary_result