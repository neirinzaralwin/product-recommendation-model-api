from fastapi import FastAPI
# from app.routes import recommendation
from app.routes import recommendation

app = FastAPI(
    title="Product Recommendation API",
    description="API for getting product recommendations based on content similarity",
    version="1.0.0"
)

app.include_router(recommendation.router, tags=["recommendations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)