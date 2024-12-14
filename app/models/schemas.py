from typing import List, Optional, Any
from pydantic import BaseModel, Field

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

class ErrorResponse(BaseModel):
    statusCode: int = Field(..., example=400)
    message: str = Field(..., example="Bad request")
