from fastapi import FastAPI, HTTPException
from app.models import RecommendationRequest, RecommendationResponse, ProductRecommendation
from app.utils import prepare_data
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = FastAPI(
    title="Product Recommendation API",
    description="API for getting product recommendations based on content similarity",
    version="1.0.0"
)

# Global variables for model
tfidf_matrix = None
cosine_sim = None
indices = None
titles = None

@app.on_event("startup")
async def initialize_model():
    global tfidf_matrix, cosine_sim, indices, titles

    # Read data
   
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(current_dir), "data", "raw", "flipkart_sample.csv") 

    df = pd.read_csv(data_path, na_values=["No rating available"])

    # Prepare data
    smd = prepare_data(df)

    # Create TF-IDF matrix
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=1, stop_words='english')
    tfidf_matrix = tf.fit_transform(smd['all_meta'])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Reset index and create indices mapping
    smd = smd.reset_index()
    titles = smd['product_name']
    indices = pd.Series(smd.index, index=smd['product_name'])

def get_recommendations(title: str, num_recommendations: int = 5):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:num_recommendations+1]
        product_indices = [i[0] for i in sim_scores]
        recommendations = titles.iloc[product_indices].tolist()
        similarity_scores = [score[1] for score in sim_scores]
        return recommendations, similarity_scores
    except KeyError:
        return [], []

@app.get("/")
async def root():
    return {"message": "Welcome to the Product Recommendation API"}

@app.post("/predict", response_model=RecommendationResponse)
async def predict(request: RecommendationRequest):
    try:
        recommendations, similarity_scores = get_recommendations(
            request.product_name, 
            request.num_recommendations
        )

        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail=f'Product "{request.product_name}" not found in database'
            )

        # Prepare response
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