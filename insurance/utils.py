from pymongo import MongoClient
from insurance.settings import (
    MONGO_INITDB_DATABASE,
    MONGO_INITDB_USERNAME,
    MONGO_INITDB_PASSWORD,
    MONGO_HOST
)


def get_mongo_client():
    db_name = MONGO_INITDB_DATABASE
    username = MONGO_INITDB_USERNAME
    password = MONGO_INITDB_PASSWORD
    client = MongoClient(
        host=MONGO_HOST,
        port=27017,
        serverSelectionTimeoutMS=3000,
        username=username,
        password=password
    )
    db = client[db_name]
    return db
