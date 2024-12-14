from fastapi import APIRouter
from app.models.schemas import (
    RecommendationRequest, 
    RecommendationResponse,
    ErrorResponse
)
from app.controllers.recommendation_controller import RecommendationController

router = APIRouter()
recommendation_controller = RecommendationController()

@router.post(
        "/force_update_model",
        summary="Force update model",
        description="Force update the recommendation model",
        responses={
            500: {
                "model": ErrorResponse,
                "description": "Internal server error"
            }
        }
)
async def force_update_model():
    return await recommendation_controller.force_update_model()

@router.post(
    "/predict",
    response_model=RecommendationResponse,
    summary="Get product recommendations",
    description="Get product recommendations based on a given product name.",
    responses={
        200: {
            "model": RecommendationResponse,
            "description": "Successful response"
        },
        400: {
            "model": ErrorResponse,
            "description": "Bad request"
        },
        404: {
            "model": ErrorResponse,
            "description": "Product not found"
        },
        500: {
            "model": ErrorResponse,
            "description": "Internal server error"
        }
    }
)
async def predict(request: RecommendationRequest):
    return await recommendation_controller.get_recommendations(request)