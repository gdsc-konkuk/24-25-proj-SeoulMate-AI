from flask import request

def get_user_info():
    data = request.get_json()
    user_id = data["user_id"]
    liked_place_ids = data["liked_place_ids"]
    styles = data["styles"]
    place_id = data["place_id"]

    return user_id, liked_place_ids, styles, place_id