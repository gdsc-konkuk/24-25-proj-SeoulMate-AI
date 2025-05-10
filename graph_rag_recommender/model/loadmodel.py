import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from config.env_loader import get_google_api_key

def load_embedding_model(model_name="models/embedding-001"):
    api_key = get_google_api_key()
    return GoogleGenerativeAIEmbeddings(
        model=model_name, 
        google_api_key=api_key
    )

def encode_text(model, text: str):
    return model.embed_query(text)

def load_gemini_model(model_name = "models/gemini-1.5-pro-latest"):
    api_key = get_google_api_key()
    return ChatGoogleGenerativeAI(
        model = model_name,
        google_api_key = api_key,
        temperature=0.2,
        convert_system_message_to_human=True
    )