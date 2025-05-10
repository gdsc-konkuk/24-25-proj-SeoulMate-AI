import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from langchain_core.messages import HumanMessage, AIMessage
from services.gemini_prompt import free_chat_either, fitness_score

if __name__=="__main__":
    messages_with_place = [
        HumanMessage(content="Does this place have a calm atmosphere?"),
        AIMessage(content="Yes, it's known for being quiet and peaceful, perfect for a relaxing visit."),
        HumanMessage(content="Would it be a good option for solo travelers?")
    ]

    messages_without_place = [
        HumanMessage(content="What do you think about Jeonju Hanok Village?"),
        AIMessage(content="It’s a wonderful destination if you enjoy traditional Korean architecture and food."),
        HumanMessage(content="Is it suitable for a weekend trip with family?")
    ]

    user_id="test_user_004"
    liked_place_ids=["681a1c3547c87c2d81432497", "681a1c3547c87c2d81432498"]
    styles=["Nature", "Activities"]
    place_id="681a1c3547c87c2d81432496"

    result_without_place = free_chat_either(
        user_id=user_id,
        liked_place_ids=liked_place_ids,
        styles=styles,
        place_id=None,
        messages=messages_without_place
    )

    result_with_place = free_chat_either(
        user_id=user_id,
        liked_place_ids=liked_place_ids,
        styles=styles,
        place_id=place_id,
        messages=messages_with_place
    )


    fitness_score = fitness_score(user_id, liked_place_ids, styles, place_id)

    print("Free chat without place:", result_with_place)
    print("Free chat with place: ", result_without_place)
    print("Fitness Score: ", fitness_score)
