from typing import List

from .abstract_conversation_tree import AbstractConversationTree
from .nodes import (
    SystemConversationNode, 
    UserConversationNode,
    ResponseType,
    UtteranceType
)


class ConversationTree(AbstractConversationTree):
    
    def extract_nodes_from_text(self, text) -> None:

        turn_dict = dict()

        for line in text.strip().splitlines():
            contents = line.split(":", 1)
            contents[0] = contents[0].lower()

            if (
                (
                    contents[0] == "comments"
                    and turn_dict["participant"] not in ("User", "user")
                )
                or not contents[0]
            ) and turn_dict:

                node = self.create_node(turn_dict)
                if node is not None:
                    self.node_set.add(node)
                turn_dict = dict()
            elif not contents[0]:
                # encountered a newline
                continue
            else:
                contents[1] = contents[1].strip()
                turn_dict[contents[0]] = contents[1]
    
    def create_node(self, turn_dict):

        if not turn_dict.get("participant"):
            # metadata
            self.tree_id = turn_dict["number"]
            self.topic = turn_dict["title"]

        elif turn_dict.get("participant").lower() == "user":
            # extract complex attributes
            parent_node = None
            if turn_dict["parent_turn"]:
                parent_node = self.get_node_by_id(turn_dict["parent_turn"])
            
            query_turn_dependence = []
            if turn_dict["query_turn_dependence"]:
                node_ids = turn_dict["query_turn_dependence"].split(",")
                for node_id in node_ids:
                    node_id = node_id.strip()
                    query_dependence_node = self.get_node_by_id(node_id)
                    query_turn_dependence.append(query_dependence_node)
            
            result_turn_dependence = []
            if turn_dict["result_turn_dependence"]:
                node_ids = turn_dict["result_turn_dependence"].split(",")
                for node_id in node_ids:
                    node_id = node_id.strip()
                    result_dependence_node = self.get_node_by_id(node_id)
                    result_turn_dependence.append(result_dependence_node)
            
            utterance_type = None
            if turn_dict["utterance_type"].lower() == "question":
                utterance_type = UtteranceType(1)
            elif turn_dict["utterance_type"].lower() == "revealment":
                utterance_type = UtteranceType(2)
            elif turn_dict["utterance_type"].lower() == "feedback":
                utterance_type = UtteranceType(3)
            else:
                print("Utterance type provided not valid")    

            # initialize node
            node = UserConversationNode(
                node_id = turn_dict["number"].strip(),
                utterance = turn_dict["utterance"].strip(),
                resolved_utterance = turn_dict["resolved_utterance"].strip(),
                parent_node = parent_node,
                query_turn_dependence = query_turn_dependence,
                result_turn_dependence = result_turn_dependence,
                utterance_type = utterance_type
            )

            # update parent node's children and return node
            if parent_node:
                if not parent_node.children_nodes:
                    parent_node.children_nodes = [node]
                else:
                    parent_node.children_nodes.append(node)

            return node
        
        elif turn_dict.get("participant").lower() == "system":

            parent_node = None
            if turn_dict["parent_turn"]:
                parent_node = self.get_node_by_id(turn_dict["parent_turn"])
            
            result_passage_ids = []
            if turn_dict.get("result(s)"):
                passage_ids = turn_dict["result(s)"].split(",")
                for passage_id in passage_ids:
                    result_passage_ids.append(passage_id.strip())
            
            response_type = None
            if turn_dict["response_type"].lower() == "answer":
                utterance_type = UtteranceType(1)
            elif turn_dict["response_type"].lower() == "clarification":
                utterance_type = UtteranceType(2)
            elif turn_dict["response_type"].lower() == "elicitation":
                utterance_type = UtteranceType(3)
            elif turn_dict["response_type"].lower() == "feedback":
                utterance_type = UtteranceType(3)
            elif turn_dict["response_type"].lower() == "suggestion":
                utterance_type = UtteranceType(3)
            else:
                print("Response type provided not valid") 
            
            # initialize node
            node = SystemConversationNode(
                node_id = turn_dict["number"].strip(),
                utterance = turn_dict["response"].strip(),
                parent_node = parent_node,
                response_type = response_type,
                results = result_passage_ids
            )

            # update parent node's children and return node
            if parent_node:
                if not parent_node.children_nodes:
                    parent_node.children_nodes = [node]
                else:
                    parent_node.children_nodes.append(node)

            return node

    
    def get_node_by_id(self, node_id: str):
        candidate_node = list({node for node in self.node_set if node.node_id == node_id})
        if candidate_node:
            return candidate_node[0]
        else:
            return None
    
    def generate_conversation(self, leaf_node):

        node_list = [leaf_node]
        current_node = leaf_node.parent_node

        while current_node is not None:
            node_list.append(current_node)
            current_node = current_node.parent_node
        
        node_list.reverse()
        return node_list
    
    def generate_conversations(self):
        
        leaf_nodes = list({node for node in self.node_set if not node.children_nodes})

        conversation_paths = []
        for node in leaf_nodes:
            conversation_path = self.generate_conversation(node)
            conversation_paths.append(conversation_path)
        
        return conversation_paths
