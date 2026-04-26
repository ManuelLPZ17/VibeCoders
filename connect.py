from pymongo import MongoClient

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["vibecoders"]
    return db

if __name__ == "__main__":
    db = connect_mongo()
    print("Mongo conectado")