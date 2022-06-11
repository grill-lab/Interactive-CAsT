from utils.conversation_tree import ConversationTree

def context_converter(context, prior_node_id):
    """
    Uses the CAsT text format to reformat the context into a string that 
    can be passed to rewriter as input
    """

    conversation_tree = ConversationTree()
    conversation_tree.extract_nodes_from_text(context)

    prior_node = conversation_tree.get_node_by_id(prior_node_id)
    conversation_path = conversation_tree.generate_conversation(prior_node)

    # all utterances are relevant by default
    context = [node.utterance for node in conversation_path]
    context = " ||| ".join(context)

    return context