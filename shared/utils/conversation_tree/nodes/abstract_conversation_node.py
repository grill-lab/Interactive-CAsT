from abc import ABC, abstractmethod
from typing import List

class AbstractConversationNode(ABC):

    def __init__(self, 
        node_id: str, 
        utterance: str, 
        parent_node = None,
        children_nodes = None) -> None:

        self.node_id = node_id
        self.utterance = utterance
        self.parent_node = parent_node
        self.children_nodes = children_nodes
    
    def __hash__(self):
        return hash(self.node_id)
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and self.node_id == other.node_id
        )
