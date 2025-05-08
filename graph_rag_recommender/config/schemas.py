from pydantic import BaseModel, Field
from typing import List

class Reason(BaseModel):
    id: str = Field(description="추천 장소의 ID")
    category: str = Field(description="장소의 category")
    reason: str = Field(description="사용자에게 이 장소를 추천한 이유")

class RecommendationExplanation(BaseModel):
    recommendations: List[Reason]
