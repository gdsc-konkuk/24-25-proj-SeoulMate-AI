from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

def get_google_api_key():
   return os.getenv("GOOGLE_API_KEY")

def get_neo4j_config():
    return {
        "uri": os.getenv("NEO4J_URI"),
        "username": os.getenv("NEO4J_USERNAME"),
        "password": os.getenv("NEO4J_PASSWORD")
    }
