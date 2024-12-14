from fastapi import APIRouter, HTTPException
from app.models.schemas import RecommendationRequest, RecommendationResponse, ProductRecommendation
from app.services.recommendation_service import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.get("/")
async def root():
    return {"message": "Welcome to the Product Recommendation API"}

@router.post("/predict", response_model=RecommendationResponse)
async def predict(request: RecommendationRequest):
    try:
        recommendations, similarity_scores = recommendation_service.get_recommendations(
            request.product_name, 
            request.num_recommendations
        )

        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail=f'Product "{request.product_name}" not found in database'
            )

        response = RecommendationResponse(
            status="success",
            product_name=request.product_name,
            recommendations=[
                ProductRecommendation(
                    product_name=rec,
                    similarity_score=float(score)
                ) for rec, score in zip(recommendations, similarity_scores)
            ]
        )

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )