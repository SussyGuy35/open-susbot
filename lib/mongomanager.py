from pymongo import MongoClient
from lib.sussyconfig import get_config


config = get_config()


class MongoManager:
    _client = None

    @staticmethod
    def get_client():
        if MongoManager._client is None:
            MongoManager._client = MongoClient(config.MONGO_URI)
        return MongoManager._client

    @staticmethod
    def get_database(db_name: str):
        if db_name is None:
            raise ValueError("db_name is required")
        return MongoManager.get_client()[db_name]
    
    @staticmethod
    def get_collection(collection_name: str, db_name: str):
        if db_name is None:
            raise ValueError("db_name is required")
        if collection_name is None:
            raise ValueError("collection_name is required")
        return MongoManager.get_database(db_name)[collection_name]