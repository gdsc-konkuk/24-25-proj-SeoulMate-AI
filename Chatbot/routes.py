from flask import Flask, request, Blueprint
from Chatbot.services.gemini_prompt import fitness_score, free_chat_either
from Chatbot.utils import get_user_info, get_history_and_input

chatbot = Blueprint("chatbot", __name__)

@chatbot.route("/free-chat", methods=["POST"])
def free_chat_route():
    data = request.get_json()
    user_id, liked_place_ids, styles = get_user_info(data, with_place=False)
    messages = get_history_and_input(data)

    response = free_chat_either(user_id, liked_place_ids, styles, place_id=None, messages=messages)
    return response

@chatbot.route("/free-chat-with-place", methods=["POST"])
def free_chat_with_place_route():
    data = request.get_json()
    user_id, liked_place_ids, styles, place_id = get_user_info(data, with_place=True)
    messages = get_history_and_input(data)

    response = free_chat_either(user_id, liked_place_ids, styles, place_id, messages)
    return response

@chatbot.route("/fitness-score", methods=["POST"])
def fitness_score_route():
    data = request.get_json()
    user_id, liked_place_ids, styles, place_id = get_user_info(data, with_place=True)
    response = fitness_score(user_id, liked_place_ids, styles, place_id)
    return response

## Future Implementation ##

# @chatbot.route("/when-to-visit", methods=["POST"])
# def safe_location_route():
#     user_id, liked_place_ids, styles, place_id = get_user_info()
    
    
#     return  


# @chatbot.route("/detail-info", methods=["POST"])
# def detail_info_route():
#     user_id, liked_place_ids, styles, place_id = get_user_info()
    
    
#     return 