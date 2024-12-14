from fastapi import APIRouter
from app.models.schemas import (
    RecommendationRequest, 
    RecommendationResponse,
    ErrorResponse
)
from app.controllers.recommendation_controller import RecommendationController

router = APIRouter()
recommendation_controller = RecommendationController()

@router.get(
    "/",
    summary="Root endpoint",
    description="Returns a welcome message",
    response_description="Welcome message"
)
async def root():
    return await recommendation_controller.get_welcome_message()

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