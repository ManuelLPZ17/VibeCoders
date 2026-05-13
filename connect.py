try:
    from pymongo import MongoClient
except ImportError:
    MongoClient = None

CASSANDRA_IMPORT_ERROR = None
try:
    import sys
    import types

    from cassandra import InvalidRequest
    from cassandra.io.asyncioreactor import AsyncioConnection

    # cassandra-driver 3.x still tries asyncore by default, but asyncore was
    # removed in Python 3.12. Reuse the driver's asyncio reactor instead.
    asyncore_module = types.ModuleType("cassandra.io.asyncorereactor")
    asyncore_module.AsyncoreConnection = AsyncioConnection
    sys.modules.setdefault("cassandra.io.asyncorereactor", asyncore_module)

    from cassandra.cluster import Cluster, NoHostAvailable
except Exception as exc:
    Cluster = None
    InvalidRequest = None
    NoHostAvailable = None
    CASSANDRA_IMPORT_ERROR = exc

try:
    import pydgraph
except ImportError:
    pydgraph = None


CASSANDRA_KEYSPACE = "vibecoders"


def connect_mongo():
    if MongoClient is None:
        raise RuntimeError("No se encontro pymongo. Ejecuta: pip install -r requirements.txt")
    client = MongoClient("mongodb://localhost:27017/")
    db = client["vibecoders"]
    return db


def connect_cassandra(keyspace=CASSANDRA_KEYSPACE, use_keyspace=True):
    if Cluster is None:
        raise RuntimeError(
            "No se pudo cargar cassandra-driver. "
            "Ejecuta: pip install -r requirements.txt. "
            f"Detalle: {CASSANDRA_IMPORT_ERROR}"
        )

    cluster = None
    session = None
    try:
        cluster = Cluster(["127.0.0.1"], port=9042)
        session = cluster.connect()
        if use_keyspace:
            try:
                session.set_keyspace(keyspace)
            except InvalidRequest as exc:
                session.shutdown()
                cluster.shutdown()
                raise RuntimeError(
                    f"El keyspace '{keyspace}' no existe. "
                    "Primero ejecuta la opcion P para poblar Cassandra."
                ) from exc
        return cluster, session
    except RuntimeError:
        raise
    except NoHostAvailable as exc:
        if cluster is not None:
            cluster.shutdown()
        raise RuntimeError(
            "No se pudo conectar a Cassandra en 127.0.0.1:9042. "
            "Verifica que el contenedor Docker este corriendo. "
            "Cassandra puede tardar algunos segundos en iniciar completamente."
        ) from exc
    except Exception as exc:
        if session is not None:
            session.shutdown()
        if cluster is not None:
            cluster.shutdown()
        raise RuntimeError(f"Error al conectar con Cassandra: {exc}") from exc


def connect_dgraph():
    if pydgraph is None:
        raise RuntimeError("No se encontro pydgraph. Ejecuta: pip install -r requirements.txt")
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
