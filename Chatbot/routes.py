from flask import Flask, request, Blueprint
from services.gemini_prompt import fitness_score

chatbot = Blueprint("chatbot", __name__)

def get_user_info():
    data = request.get_json()
    user_id = data["user_id"]
    liked_place_ids = data["liked_place_ids"]
    styles = data["styles"]
    place_id = data["place_id"]

    return user_id, liked_place_ids, styles, place_id

# @chatbot.route("/free-chat", methods=["POST"])
# def free_chat():
#     user_id, liked_place_ids, styles, place_id = get_user_info()
#     return 


@chatbot.route("/fitness-score", methods=["POST"])
def fitness_score():
    user_id, liked_place_ids, styles, place_id = get_user_info()
    response = fitness_score(user_id, liked_place_ids, styles, place_id)
    return response


# @chatbot.route("/when-to-visit", methods=["POST"])
# def safe_location():
#     user_id, liked_place_ids, styles, place_id = get_user_info()
    
    
#     return  


# @chatbot.route("/detail-info", methods=["POST"])
# def detail_info():
#     user_id, liked_place_ids, styles, place_id = get_user_info()
    
    
#     return 