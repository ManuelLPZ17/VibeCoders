from datetime import datetime, timezone
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["vibecoders"]


# RF03 — Progreso del estudiante por lección
# Calcula el porcentaje de avance cruzando completed_lessons con el total de lecciones del curso.
def progreso_usuario(user_id, course_id):
    pipeline = [
        {"$match": {"user_id": user_id, "course_id": course_id}},
        {
            "$lookup": {
                "from": "courses",
                "localField": "course_id",
                "foreignField": "_id",
                "as": "course"
            }
        },
        {"$unwind": "$course"},
        {
            "$project": {
                "progress_percentage": 1,
                "completed": {"$size": "$completed_lessons"},
                "total": {"$size": "$course.lessons"},
                "status": 1,
                "last_accessed_at": 1
            }
        }
    ]
    return list(db.enrollments.aggregate(pipeline))


# RF09 — Historial de cursos inscritos
# Lista todos los cursos de un usuario con su estado actual, ordenados por último acceso.
def historial_cursos(user_id):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$sort": {"last_accessed_at": -1}},
        {
            "$project": {
                "course_id": 1,
                "course_title": 1,
                "progress_percentage": 1,
                "status": 1,
                "last_accessed_at": 1
            }
        }
    ]
    return list(db.enrollments.aggregate(pipeline))


# RF08 — Certificados obtenidos por usuario
# Recupera todos los certificados de un usuario ordenados por fecha de emisión más reciente.
def certificados_usuario(user_id):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$sort": {"issue_date": -1}},
        {
            "$project": {
                "course_id": 1,
                "course_title": 1,
                "issue_date": 1,
                "verification_code": 1
            }
        }
    ]
    return list(db.certificates.aggregate(pipeline))


# RF06 — Inbox de mensajes — conversaciones activas
# Lista las conversaciones del usuario mostrando primero las que tienen mensajes no leídos,
# luego por recencia. Aprovecha el multi-key index de unread_by.
def inbox(user_id):
    pipeline = [
        {"$match": {"participants": user_id}},
        {
            "$addFields": {
                "has_unread": {"$in": [user_id, "$unread_by"]}
            }
        },
        {
            "$sort": {
                "has_unread": -1,
                "last_message.sent_at": -1
            }
        },
        {
            "$project": {
                "course_id": 1,
                "participants": 1,
                "last_message": 1,
                "has_unread": 1
            }
        }
    ]
    return list(db.conversations.aggregate(pipeline))


# RF10 — Anuncios no leídos del usuario
# Recupera los anuncios vigentes de los cursos del estudiante que aún no ha leído.
# Se cruza announcements con user_announcements para determinar cuáles ya fueron leídos.
def anuncios_no_leidos(user_id, course_ids):
    pipeline = [
        {
            "$match": {
                "course_id": {"$in": course_ids},
                "$or": [
                    {"expires_at": None},
                    {"expires_at": {"$gt": datetime.now(timezone.utc)}}
                ]
            }
        },
        {
            "$lookup": {
                "from": "user_announcements",
                "let": {"ann_id": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {"$eq": ["$announcement_id", "$$ann_id"]},
                                    {"$eq": ["$user_id", user_id]}
                                ]
                            }
                        }
                    }
                ],
                "as": "read_record"
            }
        },
        {"$match": {"read_record": {"$size": 0}}},
        {"$sort": {"priority": -1, "created_at": -1}},
        {
            "$project": {
                "title": 1,
                "body": 1,
                "priority": 1
            }
        }
    ]
    return list(db.announcements.aggregate(pipeline))


# RF10 — Reporte de engagement por anuncio
# Calcula la tasa de lectura de cada anuncio de un curso.
# Útil para que el instructor identifique qué comunicados no están llegando a sus estudiantes.
def engagement_anuncios(course_id):
    pipeline = [
        {"$match": {"course_id": course_id}},
        {
            "$lookup": {
                "from": "user_announcements",
                "localField": "_id",
                "foreignField": "announcement_id",
                "as": "reads"
            }
        },
        {
            "$project": {
                "title": 1,
                "reads": {"$size": "$reads"},
                "total_enrolled": 1,
                "read_rate": {
                    "$multiply": [
                        {"$divide": [{"$size": "$reads"}, "$total_enrolled"]},
                        100
                    ]
                }
            }
        },
        {"$sort": {"read_rate": -1}}
    ]
    return list(db.announcements.aggregate(pipeline))

