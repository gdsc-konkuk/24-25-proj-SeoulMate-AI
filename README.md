# 24-25-SeoulMate-AI

## Overview

This project consists of two main components:

- **Place Recommendation**: Recommends suitable places based on the user's profile and preferences.
- **Chatbot**: Depending on the selected chat mode, the LLM generates natural language responses using the user's conversation history, place information, and graph data.

## Place Recommendation

Recommends places based on the user's travel style and past history.

- The LLM assigns an appropriate category to each place, and a graph is constructed in the database using both the category and its embedding.
- Cosine similarity between place embeddings is calculated to create `SIMILAR_TO` edges between similar places.
- A user node is created or updated each time new user information is received.
- The system searches the graph around the user node to gather candidate places. These are passed to the LLM, which reads their natural language descriptions and selects the most suitable ones.

## Chatbot

- Free Chat: When a specific place is given, the system generates a Cypher query based on the user's history and graph exploration, then uses it to directly query the graph and chat with the user.
- Fitness Score: The LLM uses both the place and user information to evaluate how well they match and provides a suitability score along with a natural language explanation.

## Tech Stack

- Backend: Python, Flask, Langchain
- LLM: Gemini 1.5 Pro (via GoogleGenerativeAI)
- Databae: Neo4j AuraDB
- Embedding: GoogleGenerativeAIEmbeddings
- Infra: Render

## Project Structure

```
proj-SeoulMate
├─ .DS_Store
├─ Chatbot
│  ├─ routes.py
│  ├─ run_example_chatbot.py
│  ├─ schemas.py
│  ├─ services
│  │  └─ gemini_prompt.py
│  ├─ tempCodeRunnerFile.py
│  └─ utils.py
├─ README.md
├─ app.py
├─ graph_rag_recommender
│  ├─ .DS_Store
│  ├─ config
│  │  ├─ env_loader.py
│  │  └─ schemas.py
│  ├─ data
│  │  ├─ .DS_Store
│  │  ├─ places.csv
│  │  ├─ places_2.csv
│  │  └─ places_example.csv
│  ├─ graph
│  │  └─ create_graph.py
│  ├─ model
│  │  └─ loadmodel.py
│  ├─ recommend
│  │  └─ recommender.py
│  ├─ routes.py
│  └─ test
│     └─ run_example.py
└─ requirements.txt
```

## Getting Started

```bash
pyhton -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python app.py
```
