from abc import ABC, abstractmethod
from typing import List, Dict

class AbstractConversationTree(ABC):

    def __init__(self) -> None:
        self.node_set = set()
        self.tree_id = None
        self.topic = None
    
    @abstractmethod
    def extract_nodes_from_text(self, text: str) -> None:
        "Extract conversation nodes given the CAST topic template"
        pass
    
    def generate_conversations(self) -> List:
        "Return all conversation paths present in tree"
        pass
    
    def generate_conversation(self, leaf_node) -> List:
        "Return conversation path given a leaf node"
        pass
    
    def create_node(self, turn_dict: Dict):
        "Create a node from input dictionary"
        pass

    def get_node_by_id(self, node_id: str):
        "Given an id, retun node"
        pass