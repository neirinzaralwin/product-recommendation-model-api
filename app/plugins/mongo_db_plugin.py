from pymongo import MongoClient
from app.config import MONGO_URI, DATABASE_NAME


def connect_to_mongo_db(app):
    @app.on_event("startup")
    def startup_db_client():
        global client
        client = MongoClient(MONGO_URI + "/" + DATABASE_NAME)
        print("Connected to MongoDB")

    @app.on_event("shutdown")
    def shutdown_db_client():
        if client:
            client.close()
            print("Disconnected from MongoDB")
