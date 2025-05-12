from flask import Flask, request, Blueprint
from graph.create_graph import update_user_node, connect_driver
from recommend.recommender import get_top_places_for_user

recommender = Blueprint("recommender", __name__)

@recommender.route("", methods=["POST"])
def recommend():
    data = request.get_json()
    user_id = data["user_id"]
    liked_place_ids = data["liked_place_ids"]
    styles = data["styles"]
    user_lat = data["y"]
    user_long = data["x"]
    
    driver = connect_driver()
    update_user_node(driver, user_id = user_id, liked_place_ids = liked_place_ids, styles=styles)
    driver.close()
    
    # AI 추천 함수 호출
    recommended_places = get_top_places_for_user(user_id=user_id, has_history = bool(liked_place_ids), styles=styles, user_lat=user_lat, user_long=user_long, top_k=5)
    
    return recommended_places 
