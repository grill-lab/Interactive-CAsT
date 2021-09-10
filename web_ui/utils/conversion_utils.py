def context_converter(context, turns_to_use):
    """
    Uses the CAsT text format to reformat the context into a string that 
    can be passed to rewriter as input
    """

    context_arr = context.splitlines()

    turns = []

    turn = {}
    for line in context_arr:
        line_content = line.split(":", 1)

        if line_content[0].lower() == "turn":
            turn["turn"] = line_content[1].strip().split("-")[1]
        
        if line_content[0].lower() == "utterance":
            turn["utterance"] = line_content[1].strip()
        
        
        if line_content[0].lower() == "passage(s)":
            passage = line_content[1].strip()
            if passage != '':
                turn["passage"] = passage
            
            turns.append(turn)
            turn = {}
    
    
    converted_context = ''

    turn_count = 0
    total_turns = len(turns)

    for turn in turns:
        #default policy is to use the last three turns as context
        #new policy is to use all queries and as many responses as possible
        utterance = turn.get("utterance")
        passage = turn.get("passage")

        turn_str = ''

        if turn_count < total_turns - turns_to_use or passage == None:
            turn_str = "{} {} ".format(utterance, "|||")
        elif passage != None:
            turn_str = "{} {} {} {} ".format(utterance, "|||", passage, "|||")
        
        converted_context += turn_str

        turn_count += 1

    return converted_context