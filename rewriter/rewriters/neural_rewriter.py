from .abstract_rewriter import AbstractRewriter
from rewriter_pb2 import RewriteRequest, RewriteResult

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class NeuralRewriter(AbstractRewriter):

    def __init__(self) -> None:

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.rewriters = {
            # other rewriters go here
            "T5": {
                "model": AutoModelForSeq2SeqLM.from_pretrained("castorini/t5-base-canard").to(self.device),
                "tokenizer": AutoTokenizer.from_pretrained("castorini/t5-base-canard")
            }
        }

        self.model = None
        self.tokenizer = None
    
    def rewrite(self, rewrite_request, context):

        if rewrite_request.rewriter == 0:
            self.model = self.rewriters["T5"]["model"]
            self.tokenizer = self.rewriters["T5"]["tokenizer"]
        
        rewriter_input = "{} ||| {}".format(rewrite_request.query_context, rewrite_request.search_query)
        rewrite_result = RewriteResult()


        tokenized_input = self.tokenizer.encode(rewriter_input, return_tensors='pt').to(self.device)
        output_ids = self.model.generate(tokenized_input, max_length=200, num_beams=4, repetition_penalty=2.5, length_penalty=1.0, early_stopping=True).to(self.device)
        rewrite_result.rewrite = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        

        return rewrite_result