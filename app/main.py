from fastapi import FastAPI
from app.routes import recommendation_route
from app.utils.exceptions import CustomException
from app.utils.exception_handlers import custom_exception_handler, general_exception_handler

app = FastAPI(
    title="Product Recommendation API",
    description="API for getting product recommendations based on content similarity",
    version="1.0.0"
)

# Register exception handlers
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register routers
app.include_router(recommendation_route.router, tags=["recommendations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)