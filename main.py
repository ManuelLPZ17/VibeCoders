"""
main.py - Menu de consultas VibeCoders
Primero pregunta qué BD usar, luego muestra solo las queries de esa BD.
"""

from connect import connect_dgraph

MENU = {
    "MongoDB": {
        "1":  "Buscar cursos por texto, categoria e idioma",
        "2":  "Ver perfil completo de un estudiante",
        "3":  "Ver progreso de un estudiante en sus cursos",
        "4":  "Listar certificados obtenidos por un usuario",
        "5":  "Ver resenas de un curso",
        "6":  "Calcular promedio de rating por curso",
    },
    "Cassandra": {
        "7":  "Ver sesiones de estudio recientes",
        "8":  "Ver avance por leccion",
        "9":  "Ver intentos recientes de quizzes",
        "10": "Ver actividad diaria de un estudiante",
        "11": "Ver actividad reciente dentro de un curso",
        "12": "Ver entregas de tareas",
        "13": "Ver notificaciones recientes",
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
    dgraph_stub, dgraph_client = None, None

    def get_dgraph():
        nonlocal dgraph_stub, dgraph_client
        if dgraph_client is None:
            dgraph_stub, dgraph_client = connect_dgraph()
        return dgraph_client

    try:
        while True:
            show_db_selector()
            db_choice = input("\nIngresa una opcion: ").strip()

            if db_choice == "0":
                print("Saliendo.")
                break

            if db_choice.upper() == "P":
                from Dgraph.populate_dgraph import populate_dgraph
                populate_dgraph(reset=True)
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

                if db_name == "Dgraph":
                    from Dgraph.queries_dgraph import run_query
                    run_query(option, get_dgraph())
                else:
                    print("  (pendiente de implementacion)")

    finally:
        if dgraph_stub is not None:
            dgraph_stub.close()


if __name__ == "__main__":
    run_menu()