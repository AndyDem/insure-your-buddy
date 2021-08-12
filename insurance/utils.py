from pymongo import MongoClient
from insurance.settings import (
    MONGO_INITDB_DATABASE,
    MONGO_INITDB_USERNAME,
    MONGO_INITDB_PASSWORD
)


def get_mongo_client():
    db_name = MONGO_INITDB_DATABASE
    username = MONGO_INITDB_USERNAME
    password = MONGO_INITDB_PASSWORD
    client = MongoClient(
        host='127.0.0.1',
        port=27017,
        serverSelectionTimeoutMS=3000,
        username=username,
        password=password
    )
    db = client[db_name]
    print('success')
    return db
