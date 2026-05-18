import json
from datetime import datetime
from bson import ObjectId

from connect import connect_mongo
from Mongo.pipelines import (
    progreso_usuario,
    historial_cursos,
    certificados_usuario,
    inbox,
    anuncios_no_leidos,
    engagement_anuncios,
)

db = connect_mongo()


# ─── Helper de serialización ────────────────────────────────────────────────

def _serial(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"No serializable: {type(obj)}")


def _print(datos):
    if not datos:
        print("  Sin resultados.")
        return
    print(json.dumps(datos, indent=2, default=_serial, ensure_ascii=False))


def _get_user(email):
    usuario = db.users.find_one({"email": email}, {"_id": 1, "role": 1})
    if not usuario:
        print(f"  Usuario '{email}' no encontrado.")
    return usuario


def _get_course(titulo):
    curso = db.courses.find_one(
        {"title": {"$regex": titulo, "$options": "i"}},
        {"_id": 1, "title": 1}
    )
    if not curso:
        print(f"  Curso '{titulo}' no encontrado.")
    return curso


# ─── RF01 — Listar cursos publicados por instructor ─────────────────────────

def _q1_cursos_instructor():
    email = input("  Email del instructor: ").strip()
    usuario = _get_user(email)
    if not usuario:
        return
    resultados = list(db.courses.find(
        {"instructor_id": usuario["_id"], "is_published": True},
        {"title": 1, "category": 1, "language": 1, "avg_rating": 1, "created_at": 1}
    ))
    _print(resultados)


# ─── RF02 — Buscar y filtrar cursos por texto, categoria e idioma ────────────

def _q2_buscar_cursos():
    texto     = input("  Texto a buscar (ej: 'python' o 'ingles'): ").strip()
    categoria = input("  Categoria (idiomas/matematicas/tecnologia, Enter omite): ").strip() or None
    idioma    = input("  Idioma (es/en, Enter omite): ").strip() or None

    filtro = {"is_published": True, "$text": {"$search": texto}}
    if categoria:
        filtro["category"] = categoria
    if idioma:
        filtro["language"] = idioma

    proyeccion = {
        "score": {"$meta": "textScore"},
        "title": 1, "category": 1, "language": 1,
        "instructor_id": 1, "avg_rating": 1
    }
    resultados = list(
        db.courses
        .find(filtro, proyeccion)
        .sort([("score", {"$meta": "textScore"})])
    )
    _print(resultados)


# ─── RF03 — Progreso del estudiante en un curso especifico ──────────────────

def _q3_progreso_estudiante():
    email  = input("  Email del estudiante: ").strip()
    titulo = input("  Titulo del curso (o parte): ").strip()

    usuario = _get_user(email)
    if not usuario:
        return
    curso = _get_course(titulo)
    if not curso:
        return

    resultados = progreso_usuario(db, usuario["_id"], curso["_id"])
    _print(resultados)


# ─── RF04 — Materiales de apoyo adjuntos a las lecciones de un curso ────────

def _q4_materiales_curso():
    titulo = input("  Titulo del curso (o parte): ").strip()
    curso = db.courses.find_one(
        {"title": {"$regex": titulo, "$options": "i"}},
        {"title": 1, "lessons.lesson_id": 1, "lessons.title": 1, "lessons.attachments": 1}
    )
    if not curso:
        print(f"  Curso '{titulo}' no encontrado.")
        return
    _print([curso])


# ─── RF05 — Perfil completo de un usuario ───────────────────────────────────

def _q5_perfil_usuario():
    email = input("  Email del usuario: ").strip()
    usuario = db.users.find_one({"email": email}, {"hashed_password": 0})
    _print([usuario] if usuario else [])


# ─── RF06 — Inbox de mensajes directos de un usuario ───────────────────────

def _q6_inbox():
    email = input("  Email del usuario: ").strip()
    usuario = _get_user(email)
    if not usuario:
        return
    resultados = inbox(db, usuario["_id"])
    _print(resultados)


# ─── RF07 — Quizzes de un curso con criterios de aprobacion ────────────────

def _q7_quizzes_curso():
    titulo = input("  Titulo del curso (o parte): ").strip()
    curso = _get_course(titulo)
    if not curso:
        return
    resultados = list(db.quizzes.find(
        {"course_id": curso["_id"]},
        {"title": 1, "passing_score": 1, "max_attempts": 1,
         "questions.question_id": 1, "questions.text": 1, "questions.options": 1}
    ))
    _print(resultados)


# ─── RF08 — Certificados obtenidos por un usuario ───────────────────────────

def _q8_certificados():
    email = input("  Email del usuario: ").strip()
    usuario = _get_user(email)
    if not usuario:
        return
    resultados = certificados_usuario(db, usuario["_id"])
    _print(resultados)


# ─── RF09 — Historial de cursos inscritos por estudiante ───────────────────

def _q9_historial_cursos():
    email = input("  Email del estudiante: ").strip()
    usuario = _get_user(email)
    if not usuario:
        return
    resultados = historial_cursos(db, usuario["_id"])
    _print(resultados)


# ─── RF10 — Anuncios no leidos y engagement por curso ──────────────────────

def _q10_anuncios():
    print("  Opciones:")
    print("    1. Anuncios no leidos de un estudiante")
    print("    2. Reporte de engagement de un curso")
    sub = input("  Selecciona (1/2): ").strip()

    if sub == "1":
        email = input("  Email del estudiante: ").strip()
        usuario = _get_user(email)
        if not usuario:
            return
        inscripciones = db.enrollments.find(
            {"user_id": usuario["_id"]},
            {"course_id": 1}
        )
        course_ids = [e["course_id"] for e in inscripciones]
        if not course_ids:
            print("  El estudiante no tiene inscripciones.")
            return
        resultados = anuncios_no_leidos(db, usuario["_id"], course_ids)
        _print(resultados)

    elif sub == "2":
        titulo = input("  Titulo del curso (o parte): ").strip()
        curso = _get_course(titulo)
        if not curso:
            return
        resultados = engagement_anuncios(db, curso["_id"])
        _print(resultados)

    else:
        print("  Opcion invalida.")


# ─── Dispatcher ─────────────────────────────────────────────────────────────

_HANDLERS = {
    "1":  _q1_cursos_instructor,
    "2":  _q2_buscar_cursos,
    "3":  _q3_progreso_estudiante,
    "4":  _q4_materiales_curso,
    "5":  _q5_perfil_usuario,
    "6":  _q6_inbox,
    "7":  _q7_quizzes_curso,
    "8":  _q8_certificados,
    "9":  _q9_historial_cursos,
    "10": _q10_anuncios,
}


def run_query(option):
    fn = _HANDLERS.get(option)
    if fn:
        fn()
