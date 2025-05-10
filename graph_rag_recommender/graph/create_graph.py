import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from neo4j import GraphDatabase
from model.loadmodel import load_embedding_model, encode_text, load_gemini_model
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic
from config.env_loader import get_neo4j_config
from langchain_core.messages import HumanMessage
import json

def load_data():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "places_2.csv"
    return pd.read_csv(csv_path, dtype={"_id": str})

def connect_driver(): 
    neo = get_neo4j_config()
    uri = neo["uri"]
    user = neo["username"]
    password = neo["password"]

    return GraphDatabase.driver(uri, auth=(user, password))

def create_graph(driver, sim_threshold, max_distance_km):
    # insert_place(driver)
    connect_similar_places(driver,sim_threshold=sim_threshold, max_distance_km=max_distance_km)

def generate_category(description, llm):
    # 카테고리 수정 필요 -> 완료
    prompt = f"""
        Based on the following place description, classify it into only one of the following categories:
        [Activites, Nature, Shopping, SNS hot places, Culture-Art-History, Eating, Tourist spot]

        Description: "{description}"
        Just return the category names only, separated by commas. For example: "Nature, Shopping"
        """
    response = llm.invoke([HumanMessage(content=prompt)])
    raw = response.content.strip()
    categories = [c.strip() for c in raw.split(',') if c.strip()]
    return categories

def insert_place(driver):
    model = load_embedding_model()
    data = load_data()
    llm = load_gemini_model()

    with driver.session(database="neo4j") as session:
        for row in data.itertuples(index = False):
            description = row.description

            coord = json.loads(row.coordinate)
            lat = float(coord['latitude'])
            lon = float(coord['longitude'])

            embedding = encode_text(model, description)
            category = generate_category(description, llm)
            session.run(
                """
               MERGE (p:Place {id: $id})
                SET p.name = $name, 
                    p.category = $category,
                    p.latitude = $lat,
                    p.longitude = $lon,
                    p.description = $desc,
                    p.embedding = $embedding
            """,
            id=row.id,
            name=row.name,
            category= category,
            lat=lat,
            lon=lon,
            desc=row.description,
            embedding=embedding
            )

def connect_similar_places(driver, sim_threshold, max_distance_km):
    # sim_threshold 
    # max_distance_km 

    with driver.session(database = "neo4j") as session:
        result = session.run("""
            MATCH (p:Place)
            RETURN p.id AS id, p.name AS name, p.category as category, p.latitude AS lat, p.longitude AS lon, p.embedding AS embedding
        """)

        places = []
        for record in result: 
            places.append({
                "id": record["id"],
                "name": record["name"],
                "lat": record["lat"],
                "lon": record["lon"],
                "embedding": record["embedding"]
            })

        for i in range(len(places)):
            candidates = []
            for j in range(i + 1, len(places)):
                id1, id2 = places[i]["id"], places[j]["id"]
                emb1, emb2 = [places[i]["embedding"]], [places[j]["embedding"]]
                sim = cosine_similarity(emb1, emb2)[0][0]

                loc1 = (places[i]["lat"], places[i]["lon"])
                loc2 = (places[j]["lat"], places[j]["lon"])

                if sim > sim_threshold:
                    dist = geodesic(loc1, loc2).km
                    if dist < max_distance_km:
                        candidates.append((id2, sim))

            top_matches = sorted(candidates, key=lambda x: x[1], reverse=True)

            for id2, sim in top_matches:
                session.run("""
                    MATCH (p1:Place {id: $id1}), (p2:Place {id: $id2})
                    MERGE (p1)-[:SIMILAR_TO]->(p2)
                """, id1=id1, id2=id2)

def update_user_node(driver, user_id: str, liked_place_ids: list, styles: list):
    with driver.session(database="neo4j") as session:

        session.run("""
            MERGE (u:User {id: $user_id})
        """, user_id = user_id)

        session.run("""
            MATCH (u: User {id: $user_id}) - [r: HAS_STYLE] -> ()
            DELETE r
        """, user_id = user_id)

        if styles: 
            session.run("""
                MATCH (u:User {id: $user_id})
                UNWIND $styles AS style_name
                MERGE (s:Style {name: style_name})
                MERGE (u)-[:HAS_STYLE]->(s)
            """, user_id=user_id, styles=styles)
            
        session.run("""
            MATCH (u:User {id: $user_id}) - [r:LIKED] -> ()
            DELETE r
        """, user_id=user_id)

        if liked_place_ids:
            session.run("""
                MATCH (u:User {id: $user_id})
                UNWIND $liked_place_ids AS place_id
                MATCH (p:Place {id: place_id})
                MERGE (u)-[:LIKED]->(p)
            """, user_id=user_id, liked_place_ids=liked_place_ids)

if __name__=="__main__":
    driver = connect_driver()
    create_graph(driver, sim_threshold=0.80, max_distance_km=20)
    driver.close()