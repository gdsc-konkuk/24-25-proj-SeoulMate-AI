from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')

user_style = "여자친구와 함께, 자연과 산책을 좋아해"

# 사용자 선호 장소에 관한 description 추가 가능
liked_places = ["Nami Island", "Bukchon Hanok Village"]

user_parts = [user_style] + liked_places
user_embedding = model.encode(" ".join(user_parts), convert_to_tensor=True)

places = [
    {"id": 0, "name": "Seoul Forest", "desc": "A quiet park with lakes and deer.", "loc": (37.54, 127.04)},
    {"id": 1, "name": "Lotte World", "desc": "An indoor amusement park with rides.", "loc": (37.51, 127.10)},
    {"id": 2, "name": "Namsan Tower", "desc": "Great view of the city and love locks.", "loc": (37.55, 126.98)},
    {"id": 3, "name": "Itaewon", "desc": "Cultural street with global food and shops.", "loc": (37.53, 126.99)},
    {"id": 4, "name": "Cheonggyecheon", "desc": "Urban stream with walking paths.", "loc": (37.57, 127.01)},
]

place_texts = [place["desc"] for place in places]
place_embeddings = model.encode(place_texts, convert_to_tensor=True)

cos_scores = util.pytorch_cos_sim(user_embedding, place_embeddings)[0]
top_results = np.argsort(-cos_scores.cpu())[:5]

print("🔍 추천 장소:")
for idx in top_results:
    place = places[idx]
    print(f"- {place['name']} (score: {cos_scores[idx]:.4f})")