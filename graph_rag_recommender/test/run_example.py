import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from recommend.recommender import get_top_places_for_user
from graph.create_graph import update_user_node, connect_driver

from google.generativeai import list_models

if __name__=="__main__":
    # user_id = "test_user_001"
    # liked_places = ["abc123", "bcd234"]
    user_id = "test_user_002"
    liked_places = []
    style = "Nature"

    driver = connect_driver()
    update_user_node(driver, user_id = user_id, liked_place_ids = liked_places, style = style)
    driver.close()

    res = get_top_places_for_user("test_user_001", has_history= bool(liked_places))
    print(res)
