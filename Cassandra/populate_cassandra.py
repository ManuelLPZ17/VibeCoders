from datetime import date, datetime, timezone
from decimal import Decimal
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from connect import connect_cassandra  # noqa: E402


SCHEMA_PATH = os.path.join(ROOT, "Cassandra", "schema.cql")

TABLES = [
    "sessions_by_student",
    "lesson_progress_by_student_course",
    "quiz_attempts_by_student",
    "quiz_attempts_by_student_course",
    "activity_by_student_day",
    "video_events_by_student",
    "activity_by_course_day",
    "submissions_by_student_course",
    "lesson_progress_by_course_lesson",
    "notifications_by_student",
]


def _dt(year, month, day, hour, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def _read_cql_statements(path):
    statements = []
    current = []

    with open(path, encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("--"):
                continue

            current.append(raw_line)
            if line.endswith(";"):
                statement = "".join(current).strip().rstrip(";")
                statements.append(statement)
                current = []

    return statements


def apply_schema(session):
    for statement in _read_cql_statements(SCHEMA_PATH):
        session.execute(statement)
    print("Cassandra schema aplicado.")


def reset_tables(session):
    for table in TABLES:
        session.execute(f"TRUNCATE {table}")
    print("Cassandra tablas limpiadas.")


def _insert_many(session, query, rows):
    prepared = session.prepare(query)
    for row in rows:
        session.execute(prepared, row)


def populate_cassandra(reset=False):
    cluster = None
    session = None

    try:
        cluster, session = connect_cassandra(use_keyspace=False)
        apply_schema(session)
        session.set_keyspace("vibecoders")

        if reset:
            reset_tables(session)

        print("Poblando sessions_by_student...")
        _insert_many(
            session,
            """
            INSERT INTO sessions_by_student (
                student_id, session_start, session_end, course_id,
                device_type, session_duration
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                ("U001", _dt(2026, 4, 25, 18), _dt(2026, 4, 25, 19), "C001", "laptop", 60),
                ("U001", _dt(2026, 4, 24, 20), _dt(2026, 4, 24, 20, 45), "C001", "mobile", 45),
                ("U002", _dt(2026, 4, 25, 9), _dt(2026, 4, 25, 10, 15), "C002", "tablet", 75),
            ],
        )

        print("Poblando lesson_progress_by_student_course...")
        lesson_progress = [
            ("U001", "C001", "L001", Decimal("100.0"), "completed", _dt(2026, 4, 25, 18, 30)),
            ("U001", "C001", "L002", Decimal("65.5"), "in_progress", _dt(2026, 4, 25, 18, 50)),
            ("U001", "C001", "L003", Decimal("0.0"), "not_started", _dt(2026, 4, 20, 12)),
            ("U002", "C002", "L001", Decimal("100.0"), "completed", _dt(2026, 4, 24, 10)),
        ]
        _insert_many(
            session,
            """
            INSERT INTO lesson_progress_by_student_course (
                student_id, course_id, lesson_id, progress_percent,
                status, last_accessed_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            lesson_progress,
        )

        print("Poblando quiz_attempts_by_student...")
        quiz_attempts = [
            ("U001", _dt(2026, 4, 25, 19, 5), "Q001", Decimal("88.5"), 540, True),
            ("U001", _dt(2026, 4, 24, 20, 50), "Q002", Decimal("72.0"), 620, True),
            ("U002", _dt(2026, 4, 25, 10, 20), "Q001", Decimal("64.0"), 700, False),
        ]
        _insert_many(
            session,
            """
            INSERT INTO quiz_attempts_by_student (
                student_id, attempt_time, quiz_id, score, duration_seconds, passed
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            quiz_attempts,
        )

        print("Poblando quiz_attempts_by_student_course...")
        _insert_many(
            session,
            """
            INSERT INTO quiz_attempts_by_student_course (
                student_id, course_id, attempt_time, quiz_id, score, passed
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                ("U001", "C001", _dt(2026, 4, 25, 19, 5), "Q001", Decimal("88.5"), True),
                ("U001", "C001", _dt(2026, 4, 24, 20, 50), "Q002", Decimal("72.0"), True),
                ("U003", "C001", _dt(2026, 4, 25, 13, 15), "Q001", Decimal("91.0"), True),
            ],
        )

        print("Poblando activity_by_student_day...")
        student_activity = [
            ("U001", date(2026, 4, 25), _dt(2026, 4, 25, 18), "login", "C001", "L001", "platform"),
            ("U001", date(2026, 4, 25), _dt(2026, 4, 25, 18, 20), "lesson_view", "C001", "L001", "lesson_page"),
            ("U001", date(2026, 4, 25), _dt(2026, 4, 25, 18, 45), "quiz_start", "C001", "L002", "Q001"),
            ("U002", date(2026, 4, 25), _dt(2026, 4, 25, 9, 10), "lesson_view", "C002", "L001", "lesson_page"),
        ]
        _insert_many(
            session,
            """
            INSERT INTO activity_by_student_day (
                student_id, activity_date, event_time, event_type,
                course_id, lesson_id, resource_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            student_activity,
        )

        print("Poblando video_events_by_student...")
        _insert_many(
            session,
            """
            INSERT INTO video_events_by_student (
                student_id, event_time, video_id, event_type,
                watched_seconds, course_id, lesson_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                ("U001", _dt(2026, 4, 25, 18, 10), "V001", "play", 0, "C001", "L001"),
                ("U001", _dt(2026, 4, 25, 18, 28), "V001", "progress", 1080, "C001", "L001"),
                ("U001", _dt(2026, 4, 25, 18, 40), "V002", "complete", 1500, "C001", "L002"),
                ("U002", _dt(2026, 4, 25, 9, 30), "V001", "pause", 600, "C002", "L001"),
            ],
        )

        print("Poblando activity_by_course_day...")
        _insert_many(
            session,
            """
            INSERT INTO activity_by_course_day (
                course_id, activity_date, event_time, student_id,
                event_type, lesson_id, resource_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                ("C001", date(2026, 4, 25), _dt(2026, 4, 25, 18), "U001", "login", "L001", "platform"),
                ("C001", date(2026, 4, 25), _dt(2026, 4, 25, 18, 20), "U001", "lesson_view", "L001", "lesson_page"),
                ("C001", date(2026, 4, 25), _dt(2026, 4, 25, 13, 15), "U003", "quiz_attempt", "L002", "Q001"),
                ("C002", date(2026, 4, 25), _dt(2026, 4, 25, 9, 10), "U002", "lesson_view", "L001", "lesson_page"),
            ],
        )

        print("Poblando submissions_by_student_course...")
        _insert_many(
            session,
            """
            INSERT INTO submissions_by_student_course (
                student_id, course_id, submitted_at, assignment_id,
                submission_status, grade, feedback_available
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                ("U001", "C001", _dt(2026, 4, 25, 21), "A001", "submitted", Decimal("95.0"), True),
                ("U001", "C001", _dt(2026, 4, 23, 22), "A002", "graded", Decimal("88.0"), True),
                ("U002", "C002", _dt(2026, 4, 24, 16), "A001", "submitted", Decimal("0.0"), False),
            ],
        )

        print("Poblando lesson_progress_by_course_lesson...")
        _insert_many(
            session,
            """
            INSERT INTO lesson_progress_by_course_lesson (
                course_id, lesson_id, student_id, progress_percent,
                status, last_accessed_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                ("C001", "L001", "U001", Decimal("100.0"), "completed", _dt(2026, 4, 25, 18, 30)),
                ("C001", "L001", "U003", Decimal("75.0"), "in_progress", _dt(2026, 4, 25, 13, 5)),
                ("C001", "L002", "U001", Decimal("65.5"), "in_progress", _dt(2026, 4, 25, 18, 50)),
                ("C002", "L001", "U002", Decimal("100.0"), "completed", _dt(2026, 4, 24, 10)),
            ],
        )

        print("Poblando notifications_by_student...")
        _insert_many(
            session,
            """
            INSERT INTO notifications_by_student (
                student_id, notification_time, notification_id, notification_type,
                title, message, course_id, read_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    "U001",
                    _dt(2026, 4, 25, 8),
                    "N001",
                    "assignment",
                    "Nueva tarea disponible",
                    "Ya puedes entregar la tarea A001 del curso C001.",
                    "C001",
                    False,
                ),
                (
                    "U001",
                    _dt(2026, 4, 24, 15),
                    "N002",
                    "quiz",
                    "Quiz publicado",
                    "El quiz Q001 ya esta disponible.",
                    "C001",
                    True,
                ),
                (
                    "U002",
                    _dt(2026, 4, 25, 9),
                    "N003",
                    "feedback",
                    "Retroalimentacion disponible",
                    "Tu entrega A001 ya tiene comentarios.",
                    "C002",
                    False,
                ),
            ],
        )

        print("Cassandra poblado correctamente.")

    except Exception as exc:
        print(f"Error al poblar Cassandra: {exc}")
        raise
    finally:
        if session is not None:
            session.shutdown()
        if cluster is not None:
            cluster.shutdown()


if __name__ == "__main__":
    populate_cassandra(reset=True)
