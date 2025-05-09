def run_example():
    messages = [
        HumanMessage(content="경복궁 어때?"),
        AIMessage(content="전통문화에 관심이 많다면 좋은 선택이에요."),
        HumanMessage(content="혼자 가도 괜찮을까?")
    ]

    result = free_chat_either(
        user_id="abc123",
        liked_place_ids=["bvc123", "fkg123"],
        styles=["Nature", "Activities"],
        place_id="a1b2c3",
        messages=messages
    )

    print("🤖 Assistant:", result["reply"])
