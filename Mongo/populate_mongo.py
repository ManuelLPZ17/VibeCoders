from datetime import datetime, timezone
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["vibecoders"]

COLECCIONES = [
    "users", "courses", "enrollments", "quizzes", "certificates",
    "conversations", "messages", "announcements", "user_announcements"
]


def drop_all():
    for col in COLECCIONES:
        db[col].drop()
    print("  MongoDB: colecciones eliminadas.")


def populate_mongo(reset=True):
    if reset:
        drop_all()

    print("  MongoDB: insertando datos...")

    # ─── 1. USUARIOS ────────────────────────────────────────────────────────
    # RF05 — Registro de usuarios con rol instructor o student
    laura_id  = ObjectId()
    jose_id   = ObjectId()
    ana_t_id  = ObjectId()
    carlos_id = ObjectId()
    ana_p_id  = ObjectId()
    luis_id   = ObjectId()
    maria_id  = ObjectId()
    jorge_id  = ObjectId()

    db.users.insert_many([
        {
            "_id": laura_id,
            "username": "laura_martinez",
            "email": "laura@vibecoders.mx",
            "hashed_password": "$2b$12$LauraMtzHash...",
            "role": "instructor",
            "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc)
        },
        {
            "_id": jose_id,
            "username": "jose_ramirez",
            "email": "jose@vibecoders.mx",
            "hashed_password": "$2b$12$JoseRmzHash...",
            "role": "instructor",
            "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc)
        },
        {
            "_id": ana_t_id,
            "username": "ana_torres",
            "email": "ana.torres@vibecoders.mx",
            "hashed_password": "$2b$12$AnaTrrsHash...",
            "role": "instructor",
            "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc)
        },
        {
            "_id": carlos_id,
            "username": "carlos_lopez",
            "email": "carlos@vibecoders.mx",
            "hashed_password": "$2b$12$CarlosLpHash...",
            "role": "student",
            "created_at": datetime(2026, 1, 10, tzinfo=timezone.utc)
        },
        {
            "_id": ana_p_id,
            "username": "ana_perez",
            "email": "ana.perez@vibecoders.mx",
            "hashed_password": "$2b$12$AnaPerezHash...",
            "role": "student",
            "created_at": datetime(2026, 1, 10, tzinfo=timezone.utc)
        },
        {
            "_id": luis_id,
            "username": "luis_torres",
            "email": "luis@vibecoders.mx",
            "hashed_password": "$2b$12$LuisTrrsHash...",
            "role": "student",
            "created_at": datetime(2026, 1, 12, tzinfo=timezone.utc)
        },
        {
            "_id": maria_id,
            "username": "maria_garcia",
            "email": "maria@vibecoders.mx",
            "hashed_password": "$2b$12$MariaGrcHash...",
            "role": "student",
            "created_at": datetime(2026, 1, 15, tzinfo=timezone.utc)
        },
        {
            "_id": jorge_id,
            "username": "jorge_mendez",
            "email": "jorge@vibecoders.mx",
            "hashed_password": "$2b$12$JorgeMndHash...",
            "role": "student",
            "created_at": datetime(2026, 1, 20, tzinfo=timezone.utc)
        },
    ])
    print(f"    users            : {db.users.count_documents({})} documentos")

    # ─── 2. CURSOS con lecciones y materiales adjuntos ──────────────────────
    # RF01 — Crear y publicar cursos
    # RF04 — Materiales de apoyo embebidos en lessons[]
    ia1, ia2, ia3 = "les_ia_001", "les_ia_002", "les_ia_003"
    mb1, mb2, mb3 = "les_mb_001", "les_mb_002", "les_mb_003"
    pw1, pw2, pw3 = "les_pw_001", "les_pw_002", "les_pw_003"
    pa1, pa2, pa3 = "les_pa_001", "les_pa_002", "les_pa_003"

    ingles_id  = ObjectId()
    mates_id   = ObjectId()
    progweb_id = ObjectId()
    progadv_id = ObjectId()

    db.courses.insert_many([
        {
            "_id": ingles_id,
            "title": "Ingles 1A",
            "description": "Fundamentos del idioma ingles para principiantes absolutos.",
            "category": "idiomas",
            "language": "es",
            "instructor_id": laura_id,
            "is_published": True,
            "avg_rating": 4.5,
            "created_at": datetime(2026, 1, 5, tzinfo=timezone.utc),
            "lessons": [
                {
                    "lesson_id": ia1,
                    "title": "Saludos y presentaciones",
                    "content": "Aprende a saludar y presentarte en ingles de forma natural.",
                    "attachments": [
                        {
                            "attachment_id": "att_ia_001",
                            "title": "Guia de saludos",
                            "type": "pdf",
                            "url": "https://storage.vibecoders.mx/ingles/guia_saludos.pdf",
                            "uploaded_at": datetime(2026, 1, 6, tzinfo=timezone.utc)
                        }
                    ]
                },
                {
                    "lesson_id": ia2,
                    "title": "Vocabulario basico",
                    "content": "Las 200 palabras mas comunes del ingles cotidiano.",
                    "attachments": [
                        {
                            "attachment_id": "att_ia_002",
                            "title": "Lista de vocabulario",
                            "type": "pdf",
                            "url": "https://storage.vibecoders.mx/ingles/vocabulario.pdf",
                            "uploaded_at": datetime(2026, 1, 7, tzinfo=timezone.utc)
                        }
                    ]
                },
                {
                    "lesson_id": ia3,
                    "title": "Gramatica esencial",
                    "content": "Presente simple y continuo: estructura y uso.",
                    "attachments": []
                }
            ]
        },
        {
            "_id": mates_id,
            "title": "Matematicas Basicas",
            "description": "Algebra, aritmetica y geometria explicadas desde cero.",
            "category": "matematicas",
            "language": "es",
            "instructor_id": jose_id,
            "is_published": True,
            "avg_rating": 4.8,
            "created_at": datetime(2026, 1, 5, tzinfo=timezone.utc),
            "lessons": [
                {
                    "lesson_id": mb1,
                    "title": "Numeros y operaciones",
                    "content": "Suma, resta, multiplicacion y division con ejemplos.",
                    "attachments": [
                        {
                            "attachment_id": "att_mb_001",
                            "title": "Ejercicios resueltos",
                            "type": "pdf",
                            "url": "https://storage.vibecoders.mx/mates/ejercicios.pdf",
                            "uploaded_at": datetime(2026, 1, 6, tzinfo=timezone.utc)
                        }
                    ]
                },
                {
                    "lesson_id": mb2,
                    "title": "Fracciones y decimales",
                    "content": "Operaciones con fracciones y conversion a decimales.",
                    "attachments": []
                },
                {
                    "lesson_id": mb3,
                    "title": "Geometria basica",
                    "content": "Figuras geometricas, areas y perimetros.",
                    "attachments": [
                        {
                            "attachment_id": "att_mb_002",
                            "title": "Formulario de geometria",
                            "type": "pdf",
                            "url": "https://storage.vibecoders.mx/mates/formulario_geo.pdf",
                            "uploaded_at": datetime(2026, 1, 8, tzinfo=timezone.utc)
                        }
                    ]
                }
            ]
        },
        {
            "_id": progweb_id,
            "title": "Programacion Web",
            "description": "Desarrollo web con HTML, CSS y JavaScript desde cero.",
            "category": "tecnologia",
            "language": "es",
            "instructor_id": ana_t_id,
            "is_published": True,
            "avg_rating": 4.7,
            "created_at": datetime(2026, 1, 6, tzinfo=timezone.utc),
            "lessons": [
                {
                    "lesson_id": pw1,
                    "title": "HTML y CSS",
                    "content": "Estructura semantica y estilos para paginas web.",
                    "attachments": [
                        {
                            "attachment_id": "att_pw_001",
                            "title": "Plantilla HTML base",
                            "type": "html",
                            "url": "https://storage.vibecoders.mx/web/template_base.html",
                            "uploaded_at": datetime(2026, 1, 7, tzinfo=timezone.utc)
                        }
                    ]
                },
                {
                    "lesson_id": pw2,
                    "title": "JavaScript fundamentos",
                    "content": "Variables, funciones, eventos y manipulacion del DOM.",
                    "attachments": [
                        {
                            "attachment_id": "att_pw_002",
                            "title": "Ejercicios JS",
                            "type": "pdf",
                            "url": "https://storage.vibecoders.mx/web/ejercicios_js.pdf",
                            "uploaded_at": datetime(2026, 1, 8, tzinfo=timezone.utc)
                        }
                    ]
                },
                {
                    "lesson_id": pw3,
                    "title": "APIs REST",
                    "content": "Consumo de APIs con fetch y manejo de respuestas JSON.",
                    "attachments": []
                }
            ]
        },
        {
            "_id": progadv_id,
            "title": "Programacion Avanzada",
            "description": "Programacion orientada a objetos, patrones de diseno y testing en Python.",
            "category": "tecnologia",
            "language": "es",
            "instructor_id": ana_t_id,
            "is_published": True,
            "avg_rating": 4.6,
            "created_at": datetime(2026, 1, 6, tzinfo=timezone.utc),
            "lessons": [
                {
                    "lesson_id": pa1,
                    "title": "POO en Python",
                    "content": "Clases, herencia, polimorfismo y encapsulamiento.",
                    "attachments": []
                },
                {
                    "lesson_id": pa2,
                    "title": "Patrones de diseno",
                    "content": "Singleton, Factory, Observer y Strategy aplicados en Python.",
                    "attachments": [
                        {
                            "attachment_id": "att_pa_001",
                            "title": "Catalogo de patrones",
                            "type": "pdf",
                            "url": "https://storage.vibecoders.mx/avanzada/patrones.pdf",
                            "uploaded_at": datetime(2026, 1, 9, tzinfo=timezone.utc)
                        }
                    ]
                },
                {
                    "lesson_id": pa3,
                    "title": "Testing con pytest",
                    "content": "Unit tests, fixtures y medicion de cobertura de codigo.",
                    "attachments": []
                }
            ]
        }
    ])
    print(f"    courses          : {db.courses.count_documents({})} documentos")

    # ─── 3. INSCRIPCIONES ───────────────────────────────────────────────────
    # RF03 — Progreso por leccion   RF09 — Historial de cursos inscritos
    # course_title desnormalizado para evitar lookups en historial
    db.enrollments.insert_many([
        {
            "user_id": carlos_id,
            "course_id": ingles_id,
            "course_title": "Ingles 1A",
            "completed_lessons": [ia1, ia2],
            "progress_percentage": 66.7,
            "status": "in_progress",
            "last_accessed_at": datetime(2026, 4, 20, tzinfo=timezone.utc)
        },
        {
            "user_id": carlos_id,
            "course_id": progweb_id,
            "course_title": "Programacion Web",
            "completed_lessons": [pw1, pw2, pw3],
            "progress_percentage": 100.0,
            "status": "completed",
            "last_accessed_at": datetime(2026, 3, 15, tzinfo=timezone.utc)
        },
        {
            "user_id": ana_p_id,
            "course_id": mates_id,
            "course_title": "Matematicas Basicas",
            "completed_lessons": [mb1, mb2, mb3],
            "progress_percentage": 100.0,
            "status": "completed",
            "last_accessed_at": datetime(2026, 3, 10, tzinfo=timezone.utc)
        },
        {
            "user_id": luis_id,
            "course_id": progweb_id,
            "course_title": "Programacion Web",
            "completed_lessons": [pw1],
            "progress_percentage": 33.3,
            "status": "in_progress",
            "last_accessed_at": datetime(2026, 4, 25, tzinfo=timezone.utc)
        },
        {
            "user_id": maria_id,
            "course_id": ingles_id,
            "course_title": "Ingles 1A",
            "completed_lessons": [ia1],
            "progress_percentage": 33.3,
            "status": "in_progress",
            "last_accessed_at": datetime(2026, 4, 22, tzinfo=timezone.utc)
        },
        {
            "user_id": jorge_id,
            "course_id": progadv_id,
            "course_title": "Programacion Avanzada",
            "completed_lessons": [],
            "progress_percentage": 0.0,
            "status": "in_progress",
            "last_accessed_at": datetime(2026, 4, 23, tzinfo=timezone.utc)
        }
    ])
    print(f"    enrollments      : {db.enrollments.count_documents({})} documentos")

    # ─── 4. QUIZZES ─────────────────────────────────────────────────────────
    # RF07 — Criterios de aprobacion configurables por instructor
    db.quizzes.insert_many([
        {
            "course_id": ingles_id,
            "title": "Quiz: Saludos y vocabulario",
            "passing_score": 70,
            "max_attempts": 3,
            "questions": [
                {
                    "question_id": "q_ia_001",
                    "text": "Como se dice 'Buenos dias' en ingles?",
                    "options": ["Good morning", "Good night", "Good afternoon", "Hello"],
                    "correct": "Good morning"
                },
                {
                    "question_id": "q_ia_002",
                    "text": "Cual es el plural de 'child'?",
                    "options": ["childs", "children", "childes", "child"],
                    "correct": "children"
                },
                {
                    "question_id": "q_ia_003",
                    "text": "Completa: 'She ___ a teacher.'",
                    "options": ["are", "am", "is", "be"],
                    "correct": "is"
                }
            ]
        },
        {
            "course_id": mates_id,
            "title": "Quiz: Operaciones y geometria",
            "passing_score": 70,
            "max_attempts": 3,
            "questions": [
                {
                    "question_id": "q_mb_001",
                    "text": "Cuanto es 3/4 + 1/4?",
                    "options": ["1", "4/8", "2/4", "3/8"],
                    "correct": "1"
                },
                {
                    "question_id": "q_mb_002",
                    "text": "Cuanto es el area de un cuadrado de lado 5?",
                    "options": ["20", "10", "25", "15"],
                    "correct": "25"
                },
                {
                    "question_id": "q_mb_003",
                    "text": "Cuanto es 0.5 multiplicado por 8?",
                    "options": ["2", "4", "6", "8"],
                    "correct": "4"
                }
            ]
        },
        {
            "course_id": progweb_id,
            "title": "Quiz: HTML, CSS y JavaScript",
            "passing_score": 70,
            "max_attempts": 3,
            "questions": [
                {
                    "question_id": "q_pw_001",
                    "text": "Que etiqueta se usa para un parrafo en HTML?",
                    "options": ["<div>", "<p>", "<span>", "<section>"],
                    "correct": "<p>"
                },
                {
                    "question_id": "q_pw_002",
                    "text": "Que metodo selecciona un elemento por ID en JavaScript?",
                    "options": ["querySelector", "getElementById", "getElement", "findById"],
                    "correct": "getElementById"
                },
                {
                    "question_id": "q_pw_003",
                    "text": "Que significa REST?",
                    "options": [
                        "Representational State Transfer",
                        "Remote State Transaction",
                        "Request Endpoint Syntax Tree",
                        "Resource Encoding Standard Type"
                    ],
                    "correct": "Representational State Transfer"
                }
            ]
        },
        {
            "course_id": progadv_id,
            "title": "Quiz: POO y patrones de diseno",
            "passing_score": 75,
            "max_attempts": 2,
            "questions": [
                {
                    "question_id": "q_pa_001",
                    "text": "Que patron garantiza una sola instancia de una clase?",
                    "options": ["Factory", "Observer", "Singleton", "Strategy"],
                    "correct": "Singleton"
                },
                {
                    "question_id": "q_pa_002",
                    "text": "Que representa la L en el principio SOLID?",
                    "options": [
                        "Liskov Substitution",
                        "Layer Separation",
                        "Loose Coupling",
                        "Linear Abstraction"
                    ],
                    "correct": "Liskov Substitution"
                },
                {
                    "question_id": "q_pa_003",
                    "text": "Que libreria se usa para testing en Python en este curso?",
                    "options": ["unittest", "pytest", "nose", "doctest"],
                    "correct": "pytest"
                }
            ]
        }
    ])
    print(f"    quizzes          : {db.quizzes.count_documents({})} documentos")

    # ─── 5. CERTIFICADOS ────────────────────────────────────────────────────
    # RF08 — Solo se emiten al completar un curso (status = "completed")
    # verification_code unico para validacion externa sin autenticacion
    db.certificates.insert_many([
        {
            "user_id": carlos_id,
            "course_id": progweb_id,
            "course_title": "Programacion Web",
            "issue_date": datetime(2026, 3, 16, tzinfo=timezone.utc),
            "verification_code": "VC-2026-CARLOS-WEB"
        },
        {
            "user_id": ana_p_id,
            "course_id": mates_id,
            "course_title": "Matematicas Basicas",
            "issue_date": datetime(2026, 3, 11, tzinfo=timezone.utc),
            "verification_code": "VC-2026-ANA-MAT"
        }
    ])
    print(f"    certificates     : {db.certificates.count_documents({})} documentos")

    # ─── 6. CONVERSACIONES ──────────────────────────────────────────────────
    # RF06 — Mensajes directos entre estudiante e instructor
    # last_message desnormalizado para renderizar inbox sin consultar messages
    conv1_id = ObjectId()
    conv2_id = ObjectId()
    conv3_id = ObjectId()

    db.conversations.insert_many([
        {
            "_id": conv1_id,
            "course_id": ingles_id,
            "participants": [carlos_id, laura_id],
            "last_message": {
                "body": "Profe, tengo duda con la leccion de gramatica.",
                "sender_id": carlos_id,
                "sent_at": datetime(2026, 4, 24, 15, 0, tzinfo=timezone.utc)
            },
            "unread_by": [laura_id],
            "created_at": datetime(2026, 4, 20, tzinfo=timezone.utc)
        },
        {
            "_id": conv2_id,
            "course_id": mates_id,
            "participants": [ana_p_id, jose_id],
            "last_message": {
                "body": "Excelente trabajo en el quiz, Ana!",
                "sender_id": jose_id,
                "sent_at": datetime(2026, 3, 12, 10, 0, tzinfo=timezone.utc)
            },
            "unread_by": [],
            "created_at": datetime(2026, 3, 10, tzinfo=timezone.utc)
        },
        {
            "_id": conv3_id,
            "course_id": progweb_id,
            "participants": [luis_id, ana_t_id],
            "last_message": {
                "body": "Cuando es la entrega del proyecto final?",
                "sender_id": luis_id,
                "sent_at": datetime(2026, 4, 25, 9, 0, tzinfo=timezone.utc)
            },
            "unread_by": [ana_t_id],
            "created_at": datetime(2026, 4, 15, tzinfo=timezone.utc)
        }
    ])
    print(f"    conversations    : {db.conversations.count_documents({})} documentos")

    # ─── 7. MENSAJES ────────────────────────────────────────────────────────
    # RF06 — Cada mensaje referencia su conversation_id
    db.messages.insert_many([
        {
            "conversation_id": conv1_id,
            "sender_id": carlos_id,
            "body": "Hola profe, no entiendo la diferencia entre 'do' y 'does'.",
            "attachment": None,
            "sent_at": datetime(2026, 4, 20, 14, 0, tzinfo=timezone.utc),
            "read_at": datetime(2026, 4, 20, 16, 0, tzinfo=timezone.utc)
        },
        {
            "conversation_id": conv1_id,
            "sender_id": laura_id,
            "body": "Hola Carlos! 'do' se usa con I/you/we/they y 'does' con he/she/it.",
            "attachment": None,
            "sent_at": datetime(2026, 4, 21, 9, 0, tzinfo=timezone.utc),
            "read_at": datetime(2026, 4, 21, 12, 0, tzinfo=timezone.utc)
        },
        {
            "conversation_id": conv1_id,
            "sender_id": carlos_id,
            "body": "Profe, tengo duda con la leccion de gramatica.",
            "attachment": None,
            "sent_at": datetime(2026, 4, 24, 15, 0, tzinfo=timezone.utc),
            "read_at": None
        },
        {
            "conversation_id": conv2_id,
            "sender_id": ana_p_id,
            "body": "Ya termine el modulo de fracciones, fue muy claro!",
            "attachment": None,
            "sent_at": datetime(2026, 3, 10, 15, 0, tzinfo=timezone.utc),
            "read_at": datetime(2026, 3, 10, 17, 0, tzinfo=timezone.utc)
        },
        {
            "conversation_id": conv2_id,
            "sender_id": jose_id,
            "body": "Excelente trabajo en el quiz, Ana!",
            "attachment": None,
            "sent_at": datetime(2026, 3, 12, 10, 0, tzinfo=timezone.utc),
            "read_at": datetime(2026, 3, 12, 11, 0, tzinfo=timezone.utc)
        },
        {
            "conversation_id": conv3_id,
            "sender_id": luis_id,
            "body": "Cuando es la entrega del proyecto final?",
            "attachment": {
                "filename": "captura_proyecto.png",
                "url": "https://storage.vibecoders.mx/uploads/captura_proyecto.png",
                "type": "image/png"
            },
            "sent_at": datetime(2026, 4, 25, 9, 0, tzinfo=timezone.utc),
            "read_at": None
        }
    ])
    print(f"    messages         : {db.messages.count_documents({})} documentos")

    # ─── 8. ANUNCIOS ────────────────────────────────────────────────────────
    # RF10 — Anuncios del instructor; TTL index elimina los vencidos automaticamente
    # total_enrolled guardado para calcular tasa de lectura sin consultas adicionales
    ann1_id = ObjectId()
    ann2_id = ObjectId()
    ann3_id = ObjectId()
    ann4_id = ObjectId()

    db.announcements.insert_many([
        {
            "_id": ann1_id,
            "course_id": ingles_id,
            "instructor_id": laura_id,
            "title": "Cambio de horario — Semana del 28 de abril",
            "body": "La clase del lunes 28 se mueve al miercoles 30 a las 10:00.",
            "priority": "high",
            "expires_at": datetime(2026, 5, 1, tzinfo=timezone.utc),
            "created_at": datetime(2026, 4, 24, tzinfo=timezone.utc),
            "total_enrolled": 2
        },
        {
            "_id": ann2_id,
            "course_id": mates_id,
            "instructor_id": jose_id,
            "title": "Material extra: Ejercicios de repaso publicados",
            "body": "Subi ejercicios adicionales en la seccion de recursos del curso.",
            "priority": "normal",
            "expires_at": None,
            "created_at": datetime(2026, 4, 20, tzinfo=timezone.utc),
            "total_enrolled": 1
        },
        {
            "_id": ann3_id,
            "course_id": progweb_id,
            "instructor_id": ana_t_id,
            "title": "Proyecto final: fecha limite el 10 de mayo",
            "body": "El proyecto final se entrega el 10 de mayo antes de las 23:59. Sin excepciones.",
            "priority": "urgent",
            "expires_at": datetime(2026, 5, 11, tzinfo=timezone.utc),
            "created_at": datetime(2026, 4, 25, tzinfo=timezone.utc),
            "total_enrolled": 2
        },
        {
            "_id": ann4_id,
            "course_id": progadv_id,
            "instructor_id": ana_t_id,
            "title": "Nueva leccion disponible: Testing con pytest",
            "body": "Ya esta disponible la leccion 3. Incluye ejercicios practicos con cobertura.",
            "priority": "normal",
            "expires_at": None,
            "created_at": datetime(2026, 4, 22, tzinfo=timezone.utc),
            "total_enrolled": 1
        }
    ])
    print(f"    announcements    : {db.announcements.count_documents({})} documentos")

    # ─── 9. USER_ANNOUNCEMENTS ──────────────────────────────────────────────
    # RF10 — Separado de announcements para evitar crecimiento del documento
    # con muchos estudiantes. Indice unico evita duplicados de lectura.
    db.user_announcements.insert_many([
        {
            "user_id": carlos_id,
            "announcement_id": ann1_id,
            "read_at": datetime(2026, 4, 24, 10, 0, tzinfo=timezone.utc)
        },
        {
            "user_id": ana_p_id,
            "announcement_id": ann2_id,
            "read_at": datetime(2026, 4, 20, 12, 0, tzinfo=timezone.utc)
        },
        {
            "user_id": carlos_id,
            "announcement_id": ann3_id,
            "read_at": datetime(2026, 4, 25, 14, 0, tzinfo=timezone.utc)
        }
    ])
    print(f"    user_announcements: {db.user_announcements.count_documents({})} documentos")

    # ─── 10. VERIFICACION ───────────────────────────────────────────────────
    print("\n  Verificacion MongoDB:")
    totales = {col: db[col].count_documents({}) for col in COLECCIONES}
    total = sum(totales.values())
    for col, n in totales.items():
        print(f"    {col:<22}: {n} documentos")
    print(f"    {'TOTAL':<22}: {total} documentos")
    print("  MongoDB: datos insertados correctamente.")
