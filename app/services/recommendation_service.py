import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.data_preprocessor import DataPreprocessor
from app.config import DATA_FILE, MIN_DF, NGRAM_RANGE

class RecommendationService:
    def __init__(self):
        self.preprocessor = DataPreprocessor()
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.indices = None
        self.titles = None
        self.initialize_model()

    def initialize_model(self):
        # Read and preprocess data
        df = pd.read_csv(DATA_FILE, na_values=["No rating available"])
        smd = self.preprocessor.prepare_data(df)

        # Create TF-IDF matrix
        tf = TfidfVectorizer(
            analyzer='word',
            ngram_range=NGRAM_RANGE,
            min_df=MIN_DF,
            stop_words='english'
        )
        self.tfidf_matrix = tf.fit_transform(smd['all_meta'])

        # Calculate cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

        # Reset index and create indices mapping
        smd = smd.reset_index()
        self.titles = smd['product_name']
        self.indices = pd.Series(smd.index, index=smd['product_name'])

    def get_recommendations(self, title: str, num_recommendations: int = 5):
        try:
            idx = self.indices[title]
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:num_recommendations+1]
            product_indices = [i[0] for i in sim_scores]
            recommendations = self.titles.iloc[product_indices].tolist()
            similarity_scores = [score[1] for score in sim_scores]
            return recommendations, similarity_scores
        except KeyError:
            return [], []