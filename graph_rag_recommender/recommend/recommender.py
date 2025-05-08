from config.env_loader import get_neo4j_config
from langchain_community.graphs import Neo4jGraph
from langchain_core.output_parsers import JsonOutputParser
from config.schemas import RecommendationExplanation
from langchain.prompts import PromptTemplate
from model.loadmodel import load_gemini_model

def recommend_by_style(graph: Neo4jGraph, user_id: str, top_k: int = 3):
    query = f"""
    MATCH (u:User {{id: '{user_id}'}})-[:HAS_STYLE]->(s:Style)
    MATCH (p:Place)
    WHERE s.name IN p.category
    RETURN p.id AS id, p.category AS category, p.description AS description
    LIMIT {top_k}
    """
    return graph.query(query)

def recommend_by_history(graph: Neo4jGraph, user_id: str, top_k: int = 3):
    query = f"""
    MATCH (u:User {{id: '{user_id}'}})-[:LIKED]->(p1:Place)
    MATCH (p1)-[:SIMILAR_TO]-(p2:Place)
    WHERE NOT (u)-[:LIKED]->(p2)
    RETURN DISTINCT p2.id AS id, p2.category AS category, p2.description AS description
    LIMIT {top_k}
    """
    return graph.query(query)

def get_place_recommendations(graph: Neo4jGraph, user_id: str, has_history: bool, top_k: int = 3):
    if has_history:
        return recommend_by_history(graph, user_id, top_k)
    else:
        return recommend_by_style(graph, user_id, top_k)
    

def get_top_places_for_user(user_id, has_history):
    parser = JsonOutputParser(pydantic_object= RecommendationExplanation)
    
    llm = load_gemini_model()

    neo = get_neo4j_config()
    graph = Neo4jGraph(
        url = neo["uri"],
        username = neo["username"],
        password = neo["password"],
    )

    raw_places = get_place_recommendations(graph, user_id, has_history, top_k = 3)

    prompt = PromptTemplate(
    template="""
        Given the list of places with their IDs, categories, and descriptions, briefly explain why each place would be a good recommendation for the user.
        {format_instructions}

        Place List:
        {place_list}
        """,
        input_variables=["place_list"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | llm | parser

    place_list_text = "\n".join(
        f"- id: {rec['id']}, category: {rec['category']} description: {rec['description']}" for rec in raw_places
    )

    response = chain.invoke({"place_list": place_list_text})

    return response