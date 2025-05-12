import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from recommend.recommender import get_top_places_for_user
from graph.create_graph import update_user_node, connect_driver

if __name__=="__main__":
    # user_id = "test_user_001"
    # liked_places = ["abc123", "bcd234"]
    # user_id = "test_user_002"
    # liked_places = ["681a1c3947c87c2d81432a6a"]
    # style = ["Nature", "Parents"]
    user_id = "test_user_003"
    liked_place_ids=["681a1c3547c87c2d81432499", "681a1c3547c87c2d8143249a"]
    styles = ["SNS hot places", "Lover"]
    user_lat = 37.5198332
    user_long = 126.9910426

    driver = connect_driver()
    update_user_node(driver, user_id = user_id, liked_place_ids = liked_place_ids, styles = styles)
    driver.close()

    res = get_top_places_for_user(user_id=user_id, liked_place_ids=liked_place_ids, styles=styles, user_lat=user_lat, user_long=user_long, top_k=5)
    print(res)
