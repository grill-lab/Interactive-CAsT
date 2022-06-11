from .abstract_conversation_node import AbstractConversationNode
from typing import List

class SystemConversationNode(AbstractConversationNode):

    def __init__(self, node_id: str, 
        utterance: str,
        response_type,
        parent_node = None,
        children_nodes = None,
        results = None) -> None:

        super().__init__(
            node_id=node_id, 
            utterance=utterance, parent_node=parent_node, 
            children_nodes=children_nodes
        )
        self.results = results
        self.response_type = response_type
