from pymongo import MongoClient
from cassandra.cluster import Cluster
import pydgraph

def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["vibecoders"]
    return db

def connect_cassandra():
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect("vibecoders")
    return cluster, session

def connect_dgraph():
    stub = pydgraph.DgraphClientStub("localhost:9080")
    client = pydgraph.DgraphClient(stub)
    return stub, client

if __name__ == "__main__":
    db = connect_mongo()
    print("Mongo conectado")

    cluster, session = connect_cassandra()
    print("Cassandra conectado")

    stub, client = connect_dgraph()
    print("Dgraph conectado")

    session.shutdown()
    cluster.shutdown()
    stub.close()