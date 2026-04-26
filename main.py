"""
main.py
Menú de consultas planeadas — Plataforma VibeCoders
MongoDB · Cassandra · Dgraph
Las queries aún no están implementadas.
"""

MENU = {
    "MongoDB": {
        "1":  "Buscar cursos por texto, categoria e idioma",
        "2":  "Ver perfil completo de un estudiante",
        "3":  "Ver progreso de un estudiante en sus cursos",
        "4":  "Listar certificados obtenidos por un usuario",
        "5":  "Ver reseñas de un curso",
        "6":  "Calcular promedio de rating por curso",
    },
    "Cassandra": {
        "7":  "Ver sesiones de estudio recientes de un estudiante",
        "8":  "Ver avance por leccion de un estudiante en un curso",
        "9":  "Ver intentos recientes de quizzes de un estudiante",
        "10": "Ver actividad diaria de un estudiante",
        "11": "Ver actividad reciente dentro de un curso",
        "12": "Ver entregas de tareas de un estudiante en un curso",
        "13": "Ver notificaciones recientes de un estudiante",
    },
    "Dgraph": {
        "14": "Ver cursos en los que esta inscrito un alumno y su estado",
        "15": "Ver que maestro imparte cada curso y desde cuando",
        "16": "Ver tareas asociadas a un curso con fecha limite",
        "17": "Ver tareas entregadas por un alumno con calificacion",
        "18": "Ver examenes realizados por un alumno y su resultado",
        "19": "Consultar calificaciones de un alumno en tareas y examenes",
        "20": "Ver horario de todos los cursos",
        "21": "Ver nivel de actividad de un alumno en sus cursos",
        "22": "Ver cadena de prerrequisitos de un curso",
        "23": "Ver progreso porcentual de un alumno en sus cursos",
    },
}

def show_menu():
    print("\n========================================")
    print("   Plataforma VibeCoders — Consultas")
    print("========================================")
    for db, queries in MENU.items():
        print(f"\n  [{db}]")
        for key, desc in queries.items():
            print(f"  {key:>2}. {desc}")
    print("\n   0. Salir")
    print("========================================")

def run_menu():
    # aplanar el dict para busqueda rapida
    all_queries = {k: (db, desc) for db, queries in MENU.items() for k, desc in queries.items()}

    while True:
        show_menu()
        option = input("\nIngresa una opcion: ").strip()

        if option == "0":
            print("Saliendo.")
            break

        if option in all_queries:
            db, desc = all_queries[option]
            print(f"\n  [{db}] Consulta {option}: {desc}")
            print("  (pendiente de implementacion)")
        else:
            print("\n  Opcion invalida.")

if __name__ == "__main__":
    run_menu()