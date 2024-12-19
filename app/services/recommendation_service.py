import pandas as pd
import joblib
import os
import hashlib
from datetime import datetime
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.utils.data_preprocessor import DataPreprocessor
from app.config import  MIN_DF, NGRAM_RANGE, MONGO_URI, DATABASE_NAME

class RecommendationService:
    _instance = None
    _is_initialized = False
    MODEL_DIR = "app/data/model"
    MODEL_PATH = os.path.join(MODEL_DIR, "recommendation_model.joblib")
    HASH_PATH = os.path.join(MODEL_DIR, "data_hash.txt")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecommendationService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self.preprocessor = DataPreprocessor()
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db['products']
            self.tfidf_matrix = None
            self.cosine_sim = None
            self.indices = None
            self.titles = None
            self.load_or_initialize_model()
            RecommendationService._is_initialized = True

    def fetch_data_from_mongo(self):
        try:
            documents = list(self.collection.find({}, {"_id": 0}))
            return pd.DataFrame(documents)
        except Exception as e:
            print(f"Error in fetching data from MongoDB: {str(e)}")
            raise        

    def calculate_file_hash(self):
        hash_md5 = hashlib.md5()
        try:
            documents = list(self.collection.find({}, {"_id": 0}))
            for doc in documents:
                # Convert document to string and update hash
                hash_md5.update(str(doc).encode('utf-8'))
        except Exception as e:
            print(f"Error in calculating hash from MongoDB: {str(e)}")
            raise
        return hash_md5.hexdigest()

    def save_hash(self, file_hash):
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        with open(self.HASH_PATH, 'w') as f:
            f.write(file_hash)

    def load_hash(self):
        try:
            with open(self.HASH_PATH, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def is_data_modified(self):
        current_hash = self.calculate_file_hash()
        saved_hash = self.load_hash()
        return saved_hash != current_hash

    def load_or_initialize_model(self):
        try:
            if os.path.exists(self.MODEL_PATH) and not self.is_data_modified():
                print("Loading existing model...")
                self.load_model()
            else:
                print("Data changed or no model exists. Initializing new model...")
                self.initialize_and_save_model()
        except Exception as e:
            print(f"Error in model loading/initialization: {str(e)}")
            raise

    def load_model(self):
        model_data = joblib.load(self.MODEL_PATH)
        self.tfidf_matrix = model_data['tfidf_matrix']
        self.cosine_sim = model_data['cosine_sim']
        self.indices = model_data['indices']
        self.titles = model_data['titles']
        print("Model loaded successfully")

    def initialize_and_save_model(self):
        start_time = datetime.now()
        print(f"Starting model initialization at {start_time}")

        # Read and preprocess data
        df = self.fetch_data_from_mongo()
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

        # Save model and hash
        os.makedirs(self.MODEL_DIR, exist_ok=True)
        model_data = {
            'tfidf_matrix': self.tfidf_matrix,
            'cosine_sim': self.cosine_sim,
            'indices': self.indices,
            'titles': self.titles
        }
        joblib.dump(model_data, self.MODEL_PATH)
        self.save_hash(self.calculate_file_hash())

        end_time = datetime.now()
        duration = end_time - start_time
        print(f"Model initialized and saved successfully")
        print(f"Total initialization time: {duration}")

    def get_recommendations(self, title: str, num_recommendations: int = 5):
        try:
            # Check if data has changed
            if self.is_data_modified():
                print("Data changes detected, updating model...")
                self.initialize_and_save_model()

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

    def force_model_update(self):
        print("Forcing model update...")
        self.initialize_and_save_model()