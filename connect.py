from pymongo import MongoClient
from cassandra.cluster import Cluster

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["vibecoders"]
    return db
def connect_cassandra():
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect("vibecoders")
    return cluster, session

if __name__ == "__main__":
    db = connect_mongo()
    print("Mongo conectado")
    cluster, session = connect_cassandra()
    print("Cassandra conectado")
    session.shutdown()
    cluster.shutdown()
