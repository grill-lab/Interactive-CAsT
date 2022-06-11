from .abstract_conversation_node import AbstractConversationNode
from typing import List

class UserConversationNode(AbstractConversationNode):

    def __init__(self, node_id: str, 
        utterance: str,
        resolved_utterance: str,
        utterance_type,
        parent_node = None,
        children_nodes =  None,
        query_turn_dependence: List = [],
        result_turn_dependence: List = [],
        ) -> None:

        super().__init__(
            node_id=node_id, 
            utterance=utterance, 
            parent_node=parent_node, 
            children_nodes=children_nodes
        )
        self.resolved_utterance = resolved_utterance
        self.query_turn_dependence = query_turn_dependence
        self.result_turn_dependence = result_turn_dependence
        self.utterance_type = utterance_type