"""
queries_cassandra.py — RF01-RF10 para Cassandra
Todos los IDs usan el mismo esquema que populate.py:
  estudiantes: A1-A15  |  cursos: C1-C8  |  lecciones: les_XX_00N  |  examenes: E1-E8
"""
from datetime import date, datetime, timezone


def _print_rows(rows):
    rows = list(rows)
    if not rows:
        print("  Sin resultados.")
        return
    headers = rows[0]._fields
    widths = {h: len(h) for h in headers}
    formatted = []
    for row in rows:
        vals = {h: str(getattr(row, h)) for h in headers}
        formatted.append(vals)
        for h, v in vals.items():
            widths[h] = max(widths[h], len(v))
    print("  " + " | ".join(h.ljust(widths[h]) for h in headers))
    print("  " + "-+-".join("-" * widths[h] for h in headers))
    for vals in formatted:
        print("  " + " | ".join(vals[h].ljust(widths[h]) for h in headers))


def _ask(prompt, hint=""):
    suffix = f" (ej. {hint})" if hint else ""
    return input(f"  {prompt}{suffix}: ").strip()


def _parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


# ── RF01 — Sesiones de estudio recientes por estudiante ──────────────────────
def _q1(session):
    sid = _ask("student_id", "A1")
    rows = session.execute(
        "SELECT student_id, session_start, session_end, course_id, device_type, session_duration "
        "FROM sessions_by_student WHERE student_id = %s LIMIT 10",
        (sid,)
    )
    _print_rows(rows)


# ── RF02 — Avance por leccion de un estudiante en un curso ───────────────────
def _q2(session):
    sid = _ask("student_id", "A1")
    cid = _ask("course_id",  "C1")
    rows = session.execute(
        "SELECT lesson_id, progress_percent, status, last_accessed_at "
        "FROM lesson_progress_by_student_course "
        "WHERE student_id = %s AND course_id = %s",
        (sid, cid)
    )
    _print_rows(rows)


# ── RF03 — Intentos recientes de quizzes por estudiante ─────────────────────
def _q3(session):
    sid = _ask("student_id", "A1")
    rows = session.execute(
        "SELECT quiz_id, attempt_time, score, duration_seconds, passed "
        "FROM quiz_attempts_by_student WHERE student_id = %s LIMIT 10",
        (sid,)
    )
    _print_rows(rows)


# ── RF04 — Intentos de quizzes por estudiante y curso ───────────────────────
def _q4(session):
    sid = _ask("student_id", "A1")
    cid = _ask("course_id",  "C1")
    rows = session.execute(
        "SELECT quiz_id, attempt_time, score, passed "
        "FROM quiz_attempts_by_student_course "
        "WHERE student_id = %s AND course_id = %s LIMIT 10",
        (sid, cid)
    )
    _print_rows(rows)


# ── RF05 — Actividad diaria de un estudiante ────────────────────────────────
def _q5(session):
    sid        = _ask("student_id",    "A1")
    date_str   = _ask("activity_date", "2026-05-01")
    act_date   = _parse_date(date_str)
    rows = session.execute(
        "SELECT event_time, event_type, course_id, lesson_id, resource_id "
        "FROM activity_by_student_day "
        "WHERE student_id = %s AND activity_date = %s LIMIT 20",
        (sid, act_date)
    )
    _print_rows(rows)


# ── RF06 — Eventos de video recientes por estudiante ────────────────────────
def _q6(session):
    sid = _ask("student_id", "A1")
    rows = session.execute(
        "SELECT event_time, video_id, event_type, watched_seconds, course_id, lesson_id "
        "FROM video_events_by_student WHERE student_id = %s LIMIT 20",
        (sid,)
    )
    _print_rows(rows)


# ── RF07 — Actividad reciente dentro de un curso ────────────────────────────
def _q7(session):
    cid      = _ask("course_id",     "C1")
    date_str = _ask("activity_date", "2026-05-01")
    act_date = _parse_date(date_str)
    rows = session.execute(
        "SELECT event_time, student_id, event_type, lesson_id, resource_id "
        "FROM activity_by_course_day "
        "WHERE course_id = %s AND activity_date = %s LIMIT 20",
        (cid, act_date)
    )
    _print_rows(rows)


# ── RF08 — Entregas de tareas por estudiante y curso ────────────────────────
def _q8(session):
    sid = _ask("student_id", "A1")
    cid = _ask("course_id",  "C1")
    rows = session.execute(
        "SELECT submitted_at, assignment_id, submission_status, grade, feedback_available "
        "FROM submissions_by_student_course "
        "WHERE student_id = %s AND course_id = %s LIMIT 20",
        (sid, cid)
    )
    _print_rows(rows)


# ── RF09 — Progreso de todos los estudiantes en una leccion ─────────────────
def _q9(session):
    cid = _ask("course_id",  "C1")
    lid = _ask("lesson_id",  "les_ia_001")
    rows = session.execute(
        "SELECT student_id, progress_percent, status, last_accessed_at "
        "FROM lesson_progress_by_course_lesson "
        "WHERE course_id = %s AND lesson_id = %s",
        (cid, lid)
    )
    _print_rows(rows)


# ── RF10 — Notificaciones recientes por estudiante ───────────────────────────
def _q10(session):
    sid = _ask("student_id", "A1")
    rows = session.execute(
        "SELECT notification_time, notification_id, notification_type, "
        "title, message, course_id, read_status "
        "FROM notifications_by_student WHERE student_id = %s LIMIT 10",
        (sid,)
    )
    _print_rows(rows)


_HANDLERS = {
    "1": _q1, "2": _q2, "3": _q3, "4": _q4, "5": _q5,
    "6": _q6, "7": _q7, "8": _q8, "9": _q9, "10": _q10,
}


def run_cassandra_query(option, session):
    fn = _HANDLERS.get(option)
    if fn:
        fn(session)
    else:
        print("  Opcion invalida para Cassandra.")
