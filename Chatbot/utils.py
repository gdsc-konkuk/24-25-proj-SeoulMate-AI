from langchain.schema import AIMessage, HumanMessage

def get_user_info(data, with_place = False):
    user_id = data["user_id"]
    liked_place_ids = data["liked_place_ids"]
    styles = data["styles"]

    if with_place: 
        place_id = data["place_id"]

    return user_id, liked_place_ids, styles, place_id

def get_history_and_input(data):
    history = data["history"]
    user_input = data["input"]
    messages = []
    for turn in history:
        if turn["role"] == "human":
            messages.append(HumanMessage(content=turn["content"]))
        elif turn["role"] == "ai":
            messages.append(AIMessage(content=turn["content"]))

    messages.append(HumanMessage(content=user_input))
    return messages