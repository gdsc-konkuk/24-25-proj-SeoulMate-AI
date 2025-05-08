from flask import Flask, request, Blueprint
from services.gemini_prompt import fitness_score
from utils import get_user_info

chatbot = Blueprint("chatbot", __name__)

# @chatbot.route("/free-chat", methods=["POST"])
# def free_chat_route():
#     user_id, liked_place_ids, styles, place_id = get_user_info()
#     return 


@chatbot.route("/fitness-score", methods=["POST"])
def fitness_score_route():
    user_id, liked_place_ids, styles, place_id = get_user_info()
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