"""
main.py - Menu de consultas VibeCoders
Primero pregunta qué BD usar, luego muestra solo las queries de esa BD.
"""

from connect import connect_dgraph, connect_cassandra

MENU = {
    "MongoDB": {
        "1":  "RF01 — Listar cursos publicados por instructor",
        "2":  "RF02 — Buscar cursos por texto, categoria e idioma",
        "3":  "RF03 — Ver progreso de un estudiante en un curso especifico",
        "4":  "RF04 — Ver materiales adjuntos de las lecciones de un curso",
        "5":  "RF05 — Ver perfil completo de un usuario",
        "6":  "RF06 — Ver inbox de mensajes de un usuario",
        "7":  "RF07 — Ver quizzes de un curso con criterios de aprobacion",
        "8":  "RF08 — Listar certificados obtenidos por un usuario",
        "9":  "RF09 — Ver historial de cursos inscritos por estudiante",
        "10": "RF10 — Ver anuncios no leidos y engagement por curso",
    },
    "Cassandra": {
        "1":  "RF01 — Sesiones de estudio recientes por estudiante",
        "2":  "RF02 — Avance por leccion de un estudiante en un curso",
        "3":  "RF03 — Intentos recientes de quizzes por estudiante",
        "4":  "RF04 — Intentos de quizzes por estudiante y curso",
        "5":  "RF05 — Actividad diaria de un estudiante",
        "6":  "RF06 — Eventos de video recientes por estudiante",
        "7":  "RF07 — Actividad reciente dentro de un curso",
        "8":  "RF08 — Entregas de tareas por estudiante y curso",
        "9":  "RF09 — Progreso de estudiantes por curso y leccion",
        "10": "RF10 — Notificaciones recientes por estudiante",
    },
    "Dgraph": {
        "14": "Ver cursos en que esta inscrito un alumno y su estado",
        "15": "Ver que maestro imparte cada curso y desde cuando",
        "16": "Ver tareas asociadas a un curso con fecha limite",
        "17": "Ver tareas entregadas por un alumno con calificacion",
        "18": "Ver examenes realizados por un alumno y su resultado",
        "19": "Calificaciones (tareas + examenes) de un alumno",
        "20": "Ver horario de todos los cursos",
        "21": "Nivel de actividad de un alumno en sus cursos",
        "22": "Cadena de prerrequisitos de un curso",
        "23": "Progreso porcentual de un alumno",
    },
}

DB_KEYS = list(MENU.keys())


def show_db_selector():
    print("\n========================================")
    print("   Plataforma VibeCoders")
    print("========================================")
    print("  Selecciona la base de datos:\n")
    for i, db in enumerate(DB_KEYS, 1):
        print(f"  {i}. {db}")
    print("\n  P. Poblar bases de datos (drop + load)")
    print("  0. Salir")
    print("========================================")


def show_queries_menu(db_name):
    queries = MENU[db_name]
    print(f"\n  ---- Consultas [{db_name}] ----")
    for k, desc in queries.items():
        print(f"  {k:>2}. {desc}")
    print("\n  B. Volver al menu principal")
    print("  0. Salir")
    print("  " + "-" * 36)


def run_menu():
    dgraph_stub,   dgraph_client  = None, None
    cass_cluster,  cass_session   = None, None

    def get_dgraph():
        nonlocal dgraph_stub, dgraph_client
        if dgraph_client is None:
            dgraph_stub, dgraph_client = connect_dgraph()
        return dgraph_client

    def get_cassandra():
        nonlocal cass_cluster, cass_session
        if cass_session is None:
            cass_cluster, cass_session = connect_cassandra()
        return cass_session

    try:
        while True:
            show_db_selector()
            db_choice = input("\nIngresa una opcion: ").strip()

            if db_choice == "0":
                print("Saliendo.")
                break

            if db_choice.upper() == "P":
                from populate import populate_all
                populate_all(reset=True)
                # resetear conexiones para que usen los datos nuevos
                if cass_session:
                    cass_session.shutdown(); cass_cluster.shutdown()
                    cass_cluster, cass_session = None, None
                continue

            if db_choice not in ("1", "2", "3"):
                print("\n  Opcion invalida.")
                continue

            db_name = DB_KEYS[int(db_choice) - 1]
            queries = MENU[db_name]

            while True:
                show_queries_menu(db_name)
                option = input("\nIngresa una opcion: ").strip()

                if option == "0":
                    print("Saliendo.")
                    return

                if option.upper() == "B":
                    break

                if option not in queries:
                    print(f"\n  Opcion invalida para {db_name}.")
                    continue

                print(f"\n  [{db_name}] {option}: {queries[option]}")

                if db_name == "MongoDB":
                    from Mongo.queries_mongo import run_query as run_mongo_query
                    run_mongo_query(option)

                elif db_name == "Cassandra":
                    from Cassandra.queries_cassandra import run_cassandra_query
                    run_cassandra_query(option, get_cassandra())

                elif db_name == "Dgraph":
                    from Dgraph.queries_dgraph import run_query
                    run_query(option, get_dgraph())

    finally:
        if dgraph_stub is not None:
            dgraph_stub.close()
        if cass_session is not None:
            cass_session.shutdown()
        if cass_cluster is not None:
            cass_cluster.shutdown()


if __name__ == "__main__":
    run_menu()
