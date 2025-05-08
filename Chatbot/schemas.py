from pydantic import BaseModel, Field

class FitnessScore(BaseModel):
    score: int = Field(description="Score from 0 to 100")
    explanation: str = Field(description="Short explanation why this place fits the user")
