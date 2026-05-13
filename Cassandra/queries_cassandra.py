from datetime import date
from decimal import Decimal


QUERY_CONTEXT = {
    "1": "student_id = U001",
    "2": "student_id = U001, course_id = C001",
    "3": "student_id = U001",
    "4": "student_id = U001, course_id = C001",
    "5": "student_id = U001, activity_date = 2026-04-25",
    "6": "student_id = U001",
    "7": "course_id = C001, activity_date = 2026-04-25",
    "8": "student_id = U001, course_id = C001",
    "9": "course_id = C001, lesson_id = L001",
    "10": "student_id = U001",
}


def _format_value(value):
    if isinstance(value, Decimal):
        return str(value)
    return str(value)


def _print_rows(rows):
    rows = list(rows)
    if not rows:
        print("  Sin resultados.")
        return

    headers = rows[0]._fields
    widths = {header: len(header) for header in headers}
    formatted_rows = []

    for row in rows:
        values = {header: _format_value(getattr(row, header)) for header in headers}
        formatted_rows.append(values)
        for header, value in values.items():
            widths[header] = max(widths[header], len(value))

    header_line = " | ".join(header.ljust(widths[header]) for header in headers)
    separator = "-+-".join("-" * widths[header] for header in headers)

    print("  " + header_line)
    print("  " + separator)
    for values in formatted_rows:
        print("  " + " | ".join(values[header].ljust(widths[header]) for header in headers))


def _execute(session, option, title, query, params):
    print(f"\n>> {title}")
    print(f"   Datos de prueba: {QUERY_CONTEXT.get(option, '')}")
    rows = session.execute(query, params)
    _print_rows(rows)


def run_cassandra_query(option, session):
    try:
        # RF01 - sesiones de estudio recientes por estudiante
        if option == "1":
            _execute(
                session,
                option,
                "RF01 - Sesiones de estudio recientes por estudiante",
                """
                SELECT student_id, session_start, session_end, course_id,
                       device_type, session_duration
                FROM sessions_by_student
                WHERE student_id = %s
                LIMIT 10
                """,
                ("U001",),
            )

        # RF02 - avance por leccion de un estudiante en un curso
        elif option == "2":
            _execute(
                session,
                option,
                "RF02 - Avance por leccion de un estudiante en un curso",
                """
                SELECT lesson_id, progress_percent, status, last_accessed_at
                FROM lesson_progress_by_student_course
                WHERE student_id = %s
                AND course_id = %s
                """,
                ("U001", "C001"),
            )

        # RF03 - intentos recientes de quizzes por estudiante
        elif option == "3":
            _execute(
                session,
                option,
                "RF03 - Intentos recientes de quizzes por estudiante",
                """
                SELECT quiz_id, attempt_time, score, duration_seconds, passed
                FROM quiz_attempts_by_student
                WHERE student_id = %s
                LIMIT 10
                """,
                ("U001",),
            )

        # RF04 - intentos de quizzes por estudiante y curso
        elif option == "4":
            _execute(
                session,
                option,
                "RF04 - Intentos de quizzes por estudiante y curso",
                """
                SELECT quiz_id, attempt_time, score, passed
                FROM quiz_attempts_by_student_course
                WHERE student_id = %s
                AND course_id = %s
                LIMIT 10
                """,
                ("U001", "C001"),
            )

        # RF05 - actividad diaria de un estudiante
        elif option == "5":
            _execute(
                session,
                option,
                "RF05 - Actividad diaria de un estudiante",
                """
                SELECT event_time, event_type, course_id, lesson_id, resource_id
                FROM activity_by_student_day
                WHERE student_id = %s
                AND activity_date = %s
                LIMIT 20
                """,
                ("U001", date(2026, 4, 25)),
            )

        # RF06 - eventos de video por estudiante
        elif option == "6":
            _execute(
                session,
                option,
                "RF06 - Eventos de video por estudiante",
                """
                SELECT event_time, video_id, event_type, watched_seconds,
                       course_id, lesson_id
                FROM video_events_by_student
                WHERE student_id = %s
                LIMIT 20
                """,
                ("U001",),
            )

        # RF07 - actividad reciente dentro de un curso
        elif option == "7":
            _execute(
                session,
                option,
                "RF07 - Actividad reciente dentro de un curso",
                """
                SELECT event_time, student_id, event_type, lesson_id, resource_id
                FROM activity_by_course_day
                WHERE course_id = %s
                AND activity_date = %s
                LIMIT 20
                """,
                ("C001", date(2026, 4, 25)),
            )

        # RF08 - entregas de tareas por estudiante y curso
        elif option == "8":
            _execute(
                session,
                option,
                "RF08 - Entregas de tareas por estudiante y curso",
                """
                SELECT submitted_at, assignment_id, submission_status,
                       grade, feedback_available
                FROM submissions_by_student_course
                WHERE student_id = %s
                AND course_id = %s
                LIMIT 20
                """,
                ("U001", "C001"),
            )

        # RF09 - progreso de estudiantes por curso y leccion
        elif option == "9":
            _execute(
                session,
                option,
                "RF09 - Progreso de estudiantes por curso y leccion",
                """
                SELECT student_id, progress_percent, status, last_accessed_at
                FROM lesson_progress_by_course_lesson
                WHERE course_id = %s
                AND lesson_id = %s
                """,
                ("C001", "L001"),
            )

        # RF10 - notificaciones recientes por estudiante
        elif option == "10":
            _execute(
                session,
                option,
                "RF10 - Notificaciones recientes por estudiante",
                """
                SELECT notification_time, notification_id, notification_type,
                       title, message, course_id, read_status
                FROM notifications_by_student
                WHERE student_id = %s
                LIMIT 10
                """,
                ("U001",),
            )

        else:
            print("  Opcion invalida para Cassandra.")

    except Exception as exc:
        print(f"  Error ejecutando consulta Cassandra: {exc}")
