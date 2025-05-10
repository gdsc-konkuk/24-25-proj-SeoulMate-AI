from config.env_loader import get_neo4j_config
from langchain_community.graphs import Neo4jGraph
from langchain_core.output_parsers import JsonOutputParser
from config.schemas import RecommendationExplanation
from langchain.prompts import PromptTemplate
from model.loadmodel import load_gemini_model
from geopy.distance import geodesic

def filter_places_by_distance(places, user_lat, user_lon, max_distance_km=20):
    user_loc = (user_lat, user_lon)
    filtered = []

    for place in places:
        place_loc = (place["lat"], place["long"])
        dist = geodesic(user_loc, place_loc).kilometers
        if dist < max_distance_km:
            filtered.append(place)
    
    return filtered

def recommend_by_style(graph: Neo4jGraph, user_id: str):
    query = f"""
        MATCH (u:User {{id: '{user_id}'}})-[:HAS_STYLE]->(s:Style)
        MATCH (p:Place)
        WHERE s.name IN p.category
        RETURN p.id AS id, p.category AS category, p.description AS description, p.latitude as lat, p.longitude as long
    """
    return graph.query(query)

def recommend_by_history(graph: Neo4jGraph, user_id: str):
    query = f"""
        MATCH (u:User {{id: '{user_id}'}})-[:LIKED]->(p1:Place)
        MATCH (p1)-[:SIMILAR_TO]-(p2:Place)
        WHERE NOT (u)-[:LIKED]->(p2)
        RETURN DISTINCT p2.id AS id, p2.category AS category, p2.description AS description, p.latitude as lat, p.longitude as long
    """
    return graph.query(query)

def get_place_recommendations(graph: Neo4jGraph, user_id: str, has_history: bool):
    if has_history:
        return recommend_by_history(graph, user_id)
    else:
        return recommend_by_style(graph, user_id)
    

def get_top_places_for_user(user_id, has_history, styles, user_lat, user_long, top_k=5):
    parser = JsonOutputParser(pydantic_object= RecommendationExplanation)
    
    llm = load_gemini_model()

    neo = get_neo4j_config()
    graph = Neo4jGraph(
        url = neo["uri"],
        username = neo["username"],
        password = neo["password"],
    )

    raw_places = get_place_recommendations(graph, user_id, has_history)    
    filtered_places = filter_places_by_distance(raw_places, user_lat=user_lat, user_lon=user_long)

    print(filtered_places)

    prompt = PromptTemplate(
    template="""
        You are a travel assistant helping users choose the most suitable travel destinations from a given list.

        The user prefers the following travel styles & companion information: {user_styles}

        Here is a list of candidate places. Each place includes an ID, category, and description.

        Please read the descriptions and do the following:
        - If the number of candidate places is **greater than {top_k}**, select the best {top_k} places.
        - If the number of candidate places is **{top_k} or fewer**, use all of them.
        In either case, provide a **brief explanation** for why each selected place matches the user's style and situation.

        Each place includes an ID, category, and description in JSON format.  
        Please read the descriptions and choose the top {top_k} places that best match the user's style and travel situation.  
        **When you respond, make sure to copy the "id" and "category" exactly as shown in the list.**  

        Respond in JSON format with the following structure:
        {format_instructions}

        Place List:
        {place_list}

        """,
        input_variables=["user_styles", "top_k", "place_list"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | llm | parser

    place_list_text = "\n".join(
        f'{{"id": "{rec["id"]}", "category": "{rec["category"]}", "description": "{rec["description"]}"}}'
        for rec in filtered_places
    )   

    # print(place_list_text)
    
    response = chain.invoke({
        "place_list": place_list_text,
        "user_styles": ", ".join(styles),
        "top_k": top_k
    })

    return response