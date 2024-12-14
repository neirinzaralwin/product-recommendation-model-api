from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    product_name: str
    num_recommendations: Optional[int] = 5

class ProductRecommendation(BaseModel):
    product_name: str
    similarity_score: float

class RecommendationResponse(BaseModel):
    status: str
    product_name: str
    recommendations: List[ProductRecommendation]