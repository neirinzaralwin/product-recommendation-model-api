from app.models.schemas import RecommendationRequest, RecommendationResponse, ProductRecommendation
from app.services.recommendation_service import RecommendationService
from app.utils.exceptions import CustomException

class RecommendationController:
    def __init__(self):
        self.recommendation_service = RecommendationService()    

    async def force_update_model(self):
        try:
            await self.recommendation_service.force_model_update()
            return {"status_code": 200 , "message": "Model updated successfully"}
        except Exception as e:
            raise CustomException(
                status_code=500,
                message="An unexpected error occurred in force updating model",
            )    

    async def get_recommendations(self, request: RecommendationRequest) -> RecommendationResponse:
        try:
            if not request.product_name.strip():
                raise CustomException(
                    status_code=400,
                    message="Product name cannot be empty",
                )

            if request.num_recommendations < 1:
                raise CustomException(
                    status_code=400,
                    message="Number of recommendations must be greater than 0",
                )

            recommendations, similarity_scores = self.recommendation_service.get_recommendations(
                request.product_name, 
                request.num_recommendations
            )

            if not recommendations:
                raise CustomException(
                    status_code=404,
                    message=f'Product "{request.product_name}" not found in database',
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

        except CustomException as ce:
            raise ce
        except Exception as e:
            raise CustomException(
                status_code=500,
                message="An unexpected error occurred",
            )