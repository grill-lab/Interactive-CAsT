from pyserini.hsearch import HybridSearcher
from .sparse_searcher import SparseSearcher
from .dense_searcher import DenseSearcher
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher
from .abstract_searcher import AbstractSearcher

from searcher_pb2 import SearchQuery, DocumentQuery

class SparseDenseSearcher(DenseSearcher, AbstractSearcher):

    def __init__(self):

        DenseSearcher.__init__(self)

        self.indexes = {
            'ALL' : HybridSearcher(
                SimpleDenseSearcher('../../shared/indexes/dense/dense_test', 
                            'castorini/ance-msmarco-doc-firstp'),
                SimpleSearcher('../../shared/indexes/sparse/sparse_test')
            ),
        }