from graph_rag_recommender.model import loadmodel
from langchain_core.messages import HumanMessage, SystemMessage
from graph_rag_recommender.graph.create_graph import connect_driver, update_user_node
from langchain.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from Chatbot.schemas import FitnessScore

def find_place_and_user_in_graph(driver, user_id, place_id):
    with driver.session() as session:
        style_result = session.run("""
            MATCH (u:User {id: $user_id})-[:HAS_STYLE]->(s:Style)
            OPTIONAL MATCH (u)-[:LIKED]->(p:Place)
            RETURN collect(DISTINCT s.name) AS styles, collect(DISTINCT p.category) AS liked_categories
        """, user_id=user_id).single()

        styles = style_result["styles"]
        liked_cats = style_result["liked_categories"]
        user_profile = f"The user prefers styles such as {', '.join(styles)} and has liked places in the following categories: {', '.join(liked_cats)}."

        place_description = session.run("""
            MATCH (p:Place {id: $place_id})
            RETURN p.name AS name, p.category AS category, p.description AS description
        """, place_id = place_id).single()

        rel_result = session.run("""
            MATCH (u:User {id: $user_id})
            OPTIONAL MATCH (u)-[:LIKED]->(p1:Place)-[:SIMILAR_TO]-(p2:Place {id: $place_id})
            OPTIONAL MATCH (u)-[r:LIKED]->(p2:Place {id: $place_id})
            RETURN count(r) > 0 AS directly_liked, count(p1) > 0 AS similar_liked, collect(DISTINCT p1.name) AS similar_places
        """, user_id=user_id, place_id=place_id).single()

        if rel_result["directly_liked"]:
            relationship_summary = "The user has directly liked this place before."
        elif rel_result["similar_liked"]:
            similar_names = rel_result["similar_places"]
            relationship_summary = f"The user has liked similar places such as: {', '.join(similar_names)}."
        else:
            relationship_summary = "The user has no direct or similar connections to this place."

    return user_profile, place_description, relationship_summary

def free_chat():
    
    
    return  

def fitness_score(user_id, liked_place_ids, styles, place_id):
    driver = connect_driver()
    update_user_node(driver, user_id=user_id, liked_place_ids=liked_place_ids, styles=styles)

    llm = loadmodel()
    parser = JsonOutputParser(pydantic_schema= FitnessScore)

    user_profile, place_description, relationship_summary = find_place_and_user_in_graph(driver, user_id, place_id)

    prompt = PromptTemplate(
        template ="""
        You are a travel recommendation assistant. 

        A user has the following profile:
        {user_profile}

        Here is a place: 
        {place_description}

        And here is the relationship between the user and the place:
        {relationship_summary}

        Please evaluate how well this place matches the user's preferences.

        Return your response in JSON format with the following fields:
        - score: integer (0~100)
        - explanation: string

        {format_instructions}
        """,
        input_variables=["user_profile", "place_description", "relationship_summary"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    formatted_prompt = prompt.format(
        user_profile=user_profile,
        place_description=place_description,
        relationship_summary=relationship_summary
    )

    response = llm([HumanMessage(content=formatted_prompt)])
    parsed = parser.parse(response.content)
    return parsed.dict()

def when_to_visit(user_id, liked_place_ids, styles, place_id):
    driver = connect_driver()
    update_user_node(driver, user_id=user_id, liked_place_ids=liked_place_ids, styles=styles)

    llm = loadmodel()
    
    return  


def detail_info(user_id, liked_place_ids, styles, place_id):
    driver = connect_driver()
    update_user_node(driver, user_id=user_id, liked_place_ids=liked_place_ids, styles=styles)

    llm = loadmodel()
    
    return  