"""
populate.py — fuente unica de datos para VibeCoders
Pobla MongoDB, Dgraph y Cassandra con el mismo conjunto de datos.
Uso: python populate.py
"""
import csv
import json
import os
import sys
from datetime import datetime, date, timezone

import pydgraph
from pymongo import MongoClient
from cassandra.cluster import Cluster

ROOT    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(ROOT, "data")
SCHEMA_DQL  = os.path.join(ROOT, "Dgraph", "schema.dql")
SCHEMA_CQL  = os.path.join(ROOT, "Cassandra", "schema.cql")

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 1 — DATOS CANONICOS (leidos de CSV una sola vez)
# ═══════════════════════════════════════════════════════════════════════════════

def _load_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _slug(nombre):
    return nombre.lower().replace(" ", "_").replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")


_raw_alumnos  = _load_csv("alumnos.csv")
_raw_maestros = _load_csv("maestros.csv")
_raw_cursos   = _load_csv("cursos.csv")
_raw_tareas   = _load_csv("tareas.csv")
_raw_examenes = _load_csv("examenes.csv")
_raw_certs    = _load_csv("certificados.csv")

ALUMNOS = [
    {
        "id":       r["id_alumno"],
        "nombre":   r["nombre"],
        "genero":   r["genero"],
        "username": _slug(r["nombre"]),
        "email":    f"{_slug(r['nombre'])}@vibecoders.mx",
        "role":     "student",
        "created_at": datetime(2026, 1, 10, tzinfo=timezone.utc),
    }
    for r in _raw_alumnos
]

MAESTROS = [
    {
        "id":       r["id_maestro"],
        "nombre":   r["nombre"],
        "genero":   r["genero"],
        "username": _slug(r["nombre"]),
        "email":    f"{_slug(r['nombre'])}@vibecoders.mx",
        "role":     "instructor",
        "created_at": datetime(2026, 1, 1, tzinfo=timezone.utc),
    }
    for r in _raw_maestros
]

CURSOS = [
    {
        "id":          r["id_curso"],
        "nombre":      r["nombre"],
        "categoria":   r["categoria"],
        "day_of_week": r["day_of_week"],
        "start_time":  r["start_time"],
        "end_time":    r["end_time"],
    }
    for r in _raw_cursos
]

TAREAS = [r["id_tarea"] for r in _raw_tareas]

EXAMENES = []
for _r in _raw_examenes:
    _raw = _r["preguntas"]
    _preguntas = [p.strip() for p in _raw.split(";")] if ";" in _raw else [_raw]
    EXAMENES.append({"id": _r["id_examen"], "preguntas": _preguntas})

CERTIFICADOS = [
    {"id": r["id_certificado"], "fecha": r["fecha"], "categoria": r["categoria"]}
    for r in _raw_certs
]

# ─── Relaciones compartidas ──────────────────────────────────────────────────
# (alumno_id, curso_id, enrolled_at, status, progress, last_access, sessions_count, activity_status)
INSCRIPCIONES = [
    ("A1",  "C1",  "2026-01-10T00:00:00Z", "activo",     75,  "2026-05-01T00:00:00Z", 18, "activo"),
    ("A1",  "C3",  "2026-01-15T00:00:00Z", "activo",     60,  "2026-04-28T00:00:00Z", 12, "activo"),
    ("A2",  "C1",  "2026-01-10T00:00:00Z", "activo",     50,  "2026-03-05T00:00:00Z",  5, "inactivo"),
    ("A2",  "C2",  "2026-01-12T00:00:00Z", "completado", 100, "2026-03-10T00:00:00Z", 20, "inactivo"),
    ("A3",  "C2",  "2026-01-12T00:00:00Z", "activo",     60,  "2026-04-01T00:00:00Z", 10, "activo"),
    ("A3",  "C3",  "2026-01-15T00:00:00Z", "activo",     40,  "2026-04-25T00:00:00Z",  8, "activo"),
    ("A4",  "C3",  "2026-01-20T00:00:00Z", "activo",     85,  "2026-05-02T00:00:00Z", 22, "activo"),
    ("A4",  "C4",  "2026-02-01T00:00:00Z", "activo",     30,  "2026-04-30T00:00:00Z",  7, "activo"),
    ("A5",  "C1",  "2026-01-10T00:00:00Z", "completado", 100, "2026-04-15T00:00:00Z", 25, "inactivo"),
    ("A5",  "C5",  "2026-02-05T00:00:00Z", "activo",     70,  "2026-05-05T00:00:00Z", 15, "activo"),
    ("A6",  "C2",  "2026-01-12T00:00:00Z", "activo",     45,  "2026-04-20T00:00:00Z",  9, "activo"),
    ("A6",  "C6",  "2026-02-10T00:00:00Z", "activo",     55,  "2026-05-01T00:00:00Z", 11, "activo"),
    ("A7",  "C4",  "2026-02-01T00:00:00Z", "activo",     20,  "2026-04-10T00:00:00Z",  4, "inactivo"),
    ("A7",  "C7",  "2026-01-18T00:00:00Z", "activo",     65,  "2026-05-03T00:00:00Z", 14, "activo"),
    ("A8",  "C5",  "2026-02-05T00:00:00Z", "completado", 100, "2026-04-25T00:00:00Z", 30, "inactivo"),
    ("A8",  "C8",  "2026-02-15T00:00:00Z", "activo",     50,  "2026-05-04T00:00:00Z", 10, "activo"),
    ("A9",  "C3",  "2026-01-15T00:00:00Z", "activo",     90,  "2026-05-05T00:00:00Z", 28, "activo"),
    ("A10", "C6",  "2026-02-10T00:00:00Z", "activo",     35,  "2026-04-22T00:00:00Z",  6, "inactivo"),
    ("A11", "C1",  "2026-01-10T00:00:00Z", "activo",     80,  "2026-05-02T00:00:00Z", 19, "activo"),
    ("A12", "C2",  "2026-01-12T00:00:00Z", "activo",     55,  "2026-04-18T00:00:00Z", 13, "activo"),
    ("A13", "C7",  "2026-01-18T00:00:00Z", "completado", 100, "2026-04-20T00:00:00Z", 24, "inactivo"),
    ("A14", "C8",  "2026-02-15T00:00:00Z", "activo",     45,  "2026-05-01T00:00:00Z", 11, "activo"),
    ("A15", "C6",  "2026-02-10T00:00:00Z", "activo",     60,  "2026-05-03T00:00:00Z", 16, "activo"),
]

# (maestro_id, curso_id, assigned_at)
IMPARTE = [
    ("M1", "C1", "2026-01-05T00:00:00Z"),
    ("M1", "C7", "2026-01-05T00:00:00Z"),
    ("M2", "C2", "2026-01-05T00:00:00Z"),
    ("M2", "C5", "2026-01-06T00:00:00Z"),
    ("M3", "C3", "2026-01-06T00:00:00Z"),
    ("M3", "C4", "2026-01-06T00:00:00Z"),
    ("M4", "C6", "2026-01-07T00:00:00Z"),
    ("M5", "C8", "2026-01-07T00:00:00Z"),
]

# (curso_id, tarea_id, due_date)
CONTIENE_TAREA = [
    ("C1", "T1", "2026-05-01T00:00:00Z"),
    ("C2", "T2", "2026-05-10T00:00:00Z"),
    ("C3", "T3", "2026-06-01T00:00:00Z"),
    ("C4", "T4", "2026-06-15T00:00:00Z"),
    ("C5", "T5", "2026-05-20T00:00:00Z"),
    ("C6", "T6", "2026-06-05T00:00:00Z"),
    ("C7", "T7", "2026-05-15T00:00:00Z"),
    ("C8", "T8", "2026-06-20T00:00:00Z"),
]

# (alumno_id, tarea_id, submitted_at, status, score)
ENTREGAS = [
    ("A1",  "T1", "2026-04-30T00:00:00Z", "entregado", 92),
    ("A1",  "T3", "2026-05-28T00:00:00Z", "entregado", 78),
    ("A2",  "T1", "2026-04-29T00:00:00Z", "entregado", 65),
    ("A2",  "T2", "2026-05-09T00:00:00Z", "entregado", 80),
    ("A3",  "T2", "2026-05-08T00:00:00Z", "entregado", 55),
    ("A3",  "T3", "2026-05-31T00:00:00Z", "entregado", 70),
    ("A4",  "T3", "2026-05-30T00:00:00Z", "entregado", 95),
    ("A4",  "T4", "2026-06-14T00:00:00Z", "tarde",     60),
    ("A5",  "T1", "2026-05-01T00:00:00Z", "entregado", 88),
    ("A5",  "T5", "2026-05-19T00:00:00Z", "entregado", 91),
    ("A6",  "T2", "2026-05-10T00:00:00Z", "entregado", 74),
    ("A6",  "T6", "2026-06-04T00:00:00Z", "entregado", 68),
    ("A7",  "T4", "2026-06-16T00:00:00Z", "tarde",     45),
    ("A7",  "T7", "2026-05-14T00:00:00Z", "entregado", 72),
    ("A8",  "T5", "2026-05-20T00:00:00Z", "entregado", 97),
    ("A8",  "T8", "2026-06-19T00:00:00Z", "entregado", 85),
    ("A9",  "T3", "2026-06-01T00:00:00Z", "entregado", 89),
    ("A10", "T6", "2026-06-05T00:00:00Z", "pendiente",  0),
    ("A11", "T1", "2026-05-01T00:00:00Z", "entregado", 83),
    ("A12", "T2", "2026-05-09T00:00:00Z", "entregado", 77),
    ("A13", "T7", "2026-05-15T00:00:00Z", "entregado", 94),
    ("A14", "T8", "2026-06-20T00:00:00Z", "entregado", 81),
    ("A15", "T6", "2026-06-04T00:00:00Z", "entregado", 76),
]

# (alumno_id, examen_id, attempt_date, score)
EXAMENES_REALIZADOS = [
    ("A1",  "E1", "2026-04-15T00:00:00Z", 85),
    ("A1",  "E3", "2026-05-20T00:00:00Z", 92),
    ("A2",  "E1", "2026-04-15T00:00:00Z", 60),
    ("A2",  "E2", "2026-04-16T00:00:00Z", 72),
    ("A3",  "E2", "2026-04-16T00:00:00Z", 55),
    ("A3",  "E3", "2026-05-21T00:00:00Z", 95),
    ("A4",  "E3", "2026-05-21T00:00:00Z", 88),
    ("A4",  "E4", "2026-06-10T00:00:00Z", 50),
    ("A5",  "E1", "2026-04-15T00:00:00Z", 95),
    ("A5",  "E5", "2026-05-15T00:00:00Z", 90),
    ("A6",  "E2", "2026-04-17T00:00:00Z", 68),
    ("A6",  "E6", "2026-05-30T00:00:00Z", 74),
    ("A7",  "E4", "2026-06-12T00:00:00Z", 40),
    ("A7",  "E7", "2026-05-10T00:00:00Z", 63),
    ("A8",  "E5", "2026-05-16T00:00:00Z", 98),
    ("A8",  "E8", "2026-06-15T00:00:00Z", 87),
    ("A9",  "E3", "2026-05-22T00:00:00Z", 87),
    ("A10", "E6", "2026-05-31T00:00:00Z", 58),
    ("A11", "E1", "2026-04-15T00:00:00Z", 79),
    ("A12", "E2", "2026-04-18T00:00:00Z", 77),
    ("A13", "E7", "2026-05-11T00:00:00Z", 96),
    ("A14", "E8", "2026-06-16T00:00:00Z", 82),
    ("A15", "E6", "2026-06-01T00:00:00Z", 71),
]

# (maestro_id, tarea_id)
ASIGNA_TAREA = [
    ("M1", "T1"), ("M1", "T7"),
    ("M2", "T2"), ("M2", "T5"),
    ("M3", "T3"), ("M3", "T4"),
    ("M4", "T6"), ("M5", "T8"),
]

# (maestro_id, tarea_id, score)
CALIFICA_TAREA = [
    ("M1", "T1", 90), ("M1", "T7", 82),
    ("M2", "T2", 80), ("M2", "T5", 91),
    ("M3", "T3", 70), ("M3", "T4", 60),
    ("M4", "T6", 75), ("M5", "T8", 88),
]

# (maestro_id, examen_id, score)
CALIFICA_EXAMEN = [
    ("M1", "E1", 85), ("M1", "E7", 82),
    ("M2", "E2", 60), ("M2", "E5", 90),
    ("M3", "E3", 95), ("M3", "E4", 50),
    ("M4", "E6", 75), ("M5", "E8", 88),
]

# (curso_src, curso_dst)
PREREQUISITOS = [
    ("C1", "C7"),
    ("C2", "C5"),
    ("C2", "C8"),
    ("C3", "C4"),
    ("C5", "C8"),
]

# (alumno_id, certificado_id)
OBTIENE_CERTIFICADO = [
    ("A5",  "CERT1"),
    ("A2",  "CERT2"),
    ("A4",  "CERT3"),
    ("A9",  "CERT4"),
    ("A8",  "CERT5"),
    ("A13", "CERT6"),
    ("A1",  "CERT7"),
]

# ─── Lookups derivados ────────────────────────────────────────────────────────
_instructor_by_curso = {c: m for m, c, _ in IMPARTE}
_curso_by_tarea      = {t: c for c, t, _ in CONTIENE_TAREA}
_curso_by_examen     = {f"E{i}": f"C{i}" for i in range(1, 9)}

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 2 — MONGODB
# ═══════════════════════════════════════════════════════════════════════════════

# Enriquecimiento especifico de MongoDB: lecciones y datos extra de cada curso
_CURSO_INFO = {
    "C1": {
        "description": "Fundamentos del idioma ingles para principiantes absolutos.",
        "language": "es", "avg_rating": 4.5,
        "lessons": [
            {"lesson_id": "les_ia_001", "title": "Saludos y presentaciones",
             "content": "Aprende a saludar y presentarte en ingles de forma natural.",
             "attachments": [{"attachment_id": "att_ia_001", "title": "Guia de saludos",
                              "type": "pdf", "url": "https://storage.vibecoders.mx/ingles/guia_saludos.pdf",
                              "uploaded_at": datetime(2026, 1, 6, tzinfo=timezone.utc)}]},
            {"lesson_id": "les_ia_002", "title": "Vocabulario basico",
             "content": "Las 200 palabras mas comunes del ingles cotidiano.",
             "attachments": [{"attachment_id": "att_ia_002", "title": "Lista de vocabulario",
                              "type": "pdf", "url": "https://storage.vibecoders.mx/ingles/vocabulario.pdf",
                              "uploaded_at": datetime(2026, 1, 7, tzinfo=timezone.utc)}]},
            {"lesson_id": "les_ia_003", "title": "Gramatica esencial",
             "content": "Presente simple y continuo: estructura y uso.", "attachments": []},
        ]
    },
    "C2": {
        "description": "Algebra, aritmetica y geometria explicadas desde cero.",
        "language": "es", "avg_rating": 4.8,
        "lessons": [
            {"lesson_id": "les_mb_001", "title": "Numeros y operaciones",
             "content": "Suma, resta, multiplicacion y division con ejemplos.",
             "attachments": [{"attachment_id": "att_mb_001", "title": "Ejercicios resueltos",
                              "type": "pdf", "url": "https://storage.vibecoders.mx/mates/ejercicios.pdf",
                              "uploaded_at": datetime(2026, 1, 6, tzinfo=timezone.utc)}]},
            {"lesson_id": "les_mb_002", "title": "Fracciones y decimales",
             "content": "Operaciones con fracciones y conversion a decimales.", "attachments": []},
            {"lesson_id": "les_mb_003", "title": "Geometria basica",
             "content": "Figuras geometricas, areas y perimetros.",
             "attachments": [{"attachment_id": "att_mb_002", "title": "Formulario de geometria",
                              "type": "pdf", "url": "https://storage.vibecoders.mx/mates/formulario_geo.pdf",
                              "uploaded_at": datetime(2026, 1, 8, tzinfo=timezone.utc)}]},
        ]
    },
    "C3": {
        "description": "Desarrollo web con HTML, CSS y JavaScript desde cero.",
        "language": "es", "avg_rating": 4.7,
        "lessons": [
            {"lesson_id": "les_pw_001", "title": "HTML y CSS",
             "content": "Estructura semantica y estilos para paginas web.",
             "attachments": [{"attachment_id": "att_pw_001", "title": "Plantilla HTML base",
                              "type": "html", "url": "https://storage.vibecoders.mx/web/template_base.html",
                              "uploaded_at": datetime(2026, 1, 7, tzinfo=timezone.utc)}]},
            {"lesson_id": "les_pw_002", "title": "JavaScript fundamentos",
             "content": "Variables, funciones, eventos y manipulacion del DOM.",
             "attachments": [{"attachment_id": "att_pw_002", "title": "Ejercicios JS",
                              "type": "pdf", "url": "https://storage.vibecoders.mx/web/ejercicios_js.pdf",
                              "uploaded_at": datetime(2026, 1, 8, tzinfo=timezone.utc)}]},
            {"lesson_id": "les_pw_003", "title": "APIs REST",
             "content": "Consumo de APIs con fetch y manejo de respuestas JSON.", "attachments": []},
        ]
    },
    "C4": {
        "description": "Programacion orientada a objetos, patrones de diseno y testing en Python.",
        "language": "es", "avg_rating": 4.6,
        "lessons": [
            {"lesson_id": "les_pa_001", "title": "POO en Python",
             "content": "Clases, herencia, polimorfismo y encapsulamiento.", "attachments": []},
            {"lesson_id": "les_pa_002", "title": "Patrones de diseno",
             "content": "Singleton, Factory, Observer y Strategy aplicados en Python.",
             "attachments": [{"attachment_id": "att_pa_001", "title": "Catalogo de patrones",
                              "type": "pdf", "url": "https://storage.vibecoders.mx/avanzada/patrones.pdf",
                              "uploaded_at": datetime(2026, 1, 9, tzinfo=timezone.utc)}]},
            {"lesson_id": "les_pa_003", "title": "Testing con pytest",
             "content": "Unit tests, fixtures y medicion de cobertura de codigo.", "attachments": []},
        ]
    },
    "C5": {
        "description": "Probabilidad, estadistica descriptiva e inferencial con ejemplos aplicados.",
        "language": "es", "avg_rating": 4.4,
        "lessons": [
            {"lesson_id": "les_es_001", "title": "Estadistica descriptiva",
             "content": "Media, mediana, moda y medidas de dispersion.", "attachments": []},
            {"lesson_id": "les_es_002", "title": "Probabilidad basica",
             "content": "Experimentos aleatorios, eventos y regla de Bayes.", "attachments": []},
            {"lesson_id": "les_es_003", "title": "Distribuciones estadisticas",
             "content": "Normal, binomial y Poisson con ejercicios practicos.", "attachments": []},
        ]
    },
    "C6": {
        "description": "Modelado relacional, SQL avanzado e introduccion a NoSQL.",
        "language": "es", "avg_rating": 4.7,
        "lessons": [
            {"lesson_id": "les_bd_001", "title": "Fundamentos de BD relacionales",
             "content": "Modelo entidad-relacion, normalizacion y llaves.", "attachments": []},
            {"lesson_id": "les_bd_002", "title": "SQL avanzado",
             "content": "JOINs, subconsultas, vistas e indices.", "attachments": []},
            {"lesson_id": "les_bd_003", "title": "NoSQL y bases distribuidas",
             "content": "Documentos, grafos y columnas: cuando usar cada modelo.", "attachments": []},
        ]
    },
    "C7": {
        "description": "Ingles intermedio-avanzado: tiempos verbales, escritura formal y vocabulario especializado.",
        "language": "es", "avg_rating": 4.3,
        "lessons": [
            {"lesson_id": "les_ib_001", "title": "Tiempos verbales avanzados",
             "content": "Perfect tenses, passive voice y reported speech.", "attachments": []},
            {"lesson_id": "les_ib_002", "title": "Expresiones idiomaticas",
             "content": "Los 50 phrasal verbs mas usados en contextos profesionales.", "attachments": []},
            {"lesson_id": "les_ib_003", "title": "Escritura formal",
             "content": "Emails, reportes y ensayos en ingles profesional.", "attachments": []},
        ]
    },
    "C8": {
        "description": "Limites, derivadas y sus aplicaciones en ciencias e ingenieria.",
        "language": "es", "avg_rating": 4.5,
        "lessons": [
            {"lesson_id": "les_cd_001", "title": "Limites y continuidad",
             "content": "Definicion, propiedades y calculo de limites.", "attachments": []},
            {"lesson_id": "les_cd_002", "title": "Derivadas basicas",
             "content": "Reglas de derivacion: potencia, producto, cociente y cadena.", "attachments": []},
            {"lesson_id": "les_cd_003", "title": "Aplicaciones de la derivada",
             "content": "Maximos, minimos y problemas de optimizacion.", "attachments": []},
        ]
    },
}

_LESSON_IDS_BY_CURSO = {cid: [l["lesson_id"] for l in info["lessons"]]
                         for cid, info in _CURSO_INFO.items()}

# Quiz questions por curso (una pregunta de muestra para los 4 primeros; generico para el resto)
_QUIZ_QUESTIONS = {
    "C1": [
        {"question_id": "q_ia_001", "text": "Como se dice 'Buenos dias' en ingles?",
         "options": ["Good morning", "Good night", "Good afternoon", "Hello"], "correct": "Good morning"},
        {"question_id": "q_ia_002", "text": "Cual es el plural de 'child'?",
         "options": ["childs", "children", "childes", "child"], "correct": "children"},
        {"question_id": "q_ia_003", "text": "Completa: 'She ___ a teacher.'",
         "options": ["are", "am", "is", "be"], "correct": "is"},
    ],
    "C2": [
        {"question_id": "q_mb_001", "text": "Cuanto es 3/4 + 1/4?",
         "options": ["1", "4/8", "2/4", "3/8"], "correct": "1"},
        {"question_id": "q_mb_002", "text": "Area de un cuadrado de lado 5?",
         "options": ["20", "10", "25", "15"], "correct": "25"},
        {"question_id": "q_mb_003", "text": "Cuanto es 0.5 x 8?",
         "options": ["2", "4", "6", "8"], "correct": "4"},
    ],
    "C3": [
        {"question_id": "q_pw_001", "text": "Etiqueta para parrafo en HTML?",
         "options": ["<div>", "<p>", "<span>", "<section>"], "correct": "<p>"},
        {"question_id": "q_pw_002", "text": "Metodo que selecciona por ID en JS?",
         "options": ["querySelector", "getElementById", "getElement", "findById"],
         "correct": "getElementById"},
        {"question_id": "q_pw_003", "text": "Que significa REST?",
         "options": ["Representational State Transfer", "Remote State Transaction",
                     "Request Endpoint Syntax Tree", "Resource Encoding Standard Type"],
         "correct": "Representational State Transfer"},
    ],
    "C4": [
        {"question_id": "q_pa_001", "text": "Patron que garantiza una sola instancia de una clase?",
         "options": ["Factory", "Observer", "Singleton", "Strategy"], "correct": "Singleton"},
        {"question_id": "q_pa_002", "text": "Que representa la L en SOLID?",
         "options": ["Liskov Substitution", "Layer Separation", "Loose Coupling", "Linear Abstraction"],
         "correct": "Liskov Substitution"},
        {"question_id": "q_pa_003", "text": "Libreria de testing usada en este curso?",
         "options": ["unittest", "pytest", "nose", "doctest"], "correct": "pytest"},
    ],
    "C5": [
        {"question_id": "q_es_001", "text": "Que mide la desviacion estandar?",
         "options": ["La media", "La dispersion", "El maximo", "La moda"], "correct": "La dispersion"},
    ],
    "C6": [
        {"question_id": "q_bd_001", "text": "Que es una llave primaria?",
         "options": ["Un indice unico", "Un campo que identifica univocamente cada fila",
                     "Una relacion entre tablas", "Un tipo de JOIN"], "correct": "Un campo que identifica univocamente cada fila"},
    ],
    "C7": [
        {"question_id": "q_ib_001", "text": "Que es un phrasal verb?",
         "options": ["Un verbo + preposicion", "Un sustantivo compuesto",
                     "Un adjetivo", "Un tiempo verbal"], "correct": "Un verbo + preposicion"},
    ],
    "C8": [
        {"question_id": "q_cd_001", "text": "Derivada de f(x)=x^2?",
         "options": ["2x", "x", "x^2", "2"], "correct": "2x"},
    ],
}

_QUIZ_PASSING = {"C1": 70, "C2": 70, "C3": 70, "C4": 75, "C5": 70, "C6": 70, "C7": 70, "C8": 70}
_QUIZ_ATTEMPTS = {"C4": 2}


def _dt(iso_str):
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def populate_mongo(reset=True):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["vibecoders"]

    COLECCIONES = ["users", "courses", "enrollments", "quizzes", "certificates",
                   "conversations", "messages", "announcements", "user_announcements"]

    if reset:
        for col in COLECCIONES:
            db[col].drop()
        print("  MongoDB: colecciones eliminadas.")

    print("  MongoDB: insertando datos...")

    # ── 1. USUARIOS ──────────────────────────────────────────────────────────
    users_docs = []
    for a in ALUMNOS:
        users_docs.append({
            "_id":             a["id"],
            "username":        a["username"],
            "email":           a["email"],
            "hashed_password": f"$2b$12${a['username'][:8]}Hash...",
            "role":            "student",
            "nombre":          a["nombre"],
            "genero":          a["genero"],
            "created_at":      a["created_at"],
        })
    for m in MAESTROS:
        users_docs.append({
            "_id":             m["id"],
            "username":        m["username"],
            "email":           m["email"],
            "hashed_password": f"$2b$12${m['username'][:8]}Hash...",
            "role":            "instructor",
            "nombre":          m["nombre"],
            "genero":          m["genero"],
            "created_at":      m["created_at"],
        })
    db.users.insert_many(users_docs)
    print(f"    users            : {db.users.count_documents({})} documentos")

    # ── 2. CURSOS ────────────────────────────────────────────────────────────
    course_docs = []
    for c in CURSOS:
        info = _CURSO_INFO[c["id"]]
        instructor_id = _instructor_by_curso[c["id"]]
        course_docs.append({
            "_id":          c["id"],
            "title":        c["nombre"],
            "description":  info["description"],
            "category":     c["categoria"].lower(),
            "language":     info["language"],
            "instructor_id": instructor_id,
            "is_published": True,
            "avg_rating":   info["avg_rating"],
            "day_of_week":  c["day_of_week"],
            "start_time":   c["start_time"],
            "end_time":     c["end_time"],
            "created_at":   datetime(2026, 1, 5, tzinfo=timezone.utc),
            "lessons":      info["lessons"],
        })
    db.courses.insert_many(course_docs)
    print(f"    courses          : {db.courses.count_documents({})} documentos")

    # ── 3. INSCRIPCIONES ─────────────────────────────────────────────────────
    enroll_docs = []
    for alumno_id, curso_id, enrolled_at, status, progress, last_access, _, _ in INSCRIPCIONES:
        lesson_ids = _LESSON_IDS_BY_CURSO[curso_id]
        n_completed = round(progress / 100 * len(lesson_ids))
        completed_lessons = lesson_ids[:n_completed]
        mongo_status = "completed" if status == "completado" else "in_progress"
        curso_nombre = next(c["nombre"] for c in CURSOS if c["id"] == curso_id)
        enroll_docs.append({
            "user_id":            alumno_id,
            "course_id":          curso_id,
            "course_title":       curso_nombre,
            "completed_lessons":  completed_lessons,
            "progress_percentage": float(progress),
            "status":             mongo_status,
            "last_accessed_at":   _dt(last_access),
        })
    db.enrollments.insert_many(enroll_docs)
    print(f"    enrollments      : {db.enrollments.count_documents({})} documentos")

    # ── 4. QUIZZES ───────────────────────────────────────────────────────────
    quiz_docs = []
    for c in CURSOS:
        cid = c["id"]
        quiz_docs.append({
            "course_id":    cid,
            "title":        f"Quiz: {c['nombre']}",
            "passing_score": _QUIZ_PASSING.get(cid, 70),
            "max_attempts": _QUIZ_ATTEMPTS.get(cid, 3),
            "questions":    _QUIZ_QUESTIONS.get(cid, []),
        })
    db.quizzes.insert_many(quiz_docs)
    print(f"    quizzes          : {db.quizzes.count_documents({})} documentos")

    # ── 5. CERTIFICADOS ──────────────────────────────────────────────────────
    cert_docs = []
    cert_map = {cert["id"]: cert for cert in CERTIFICADOS}
    for alumno_id, cert_id in OBTIENE_CERTIFICADO:
        cert = cert_map[cert_id]
        # busca el curso de la misma categoria que el alumno completo
        curso_completado = next(
            (c for _, c, _, st, *_ in INSCRIPCIONES if _ and st == "completado" and
             next((cu for cu in CURSOS if cu["id"] == c and cu["categoria"].lower() == cert["categoria"].lower()), None)),
            None
        )
        curso_nombre = ""
        if curso_completado:
            curso_nombre = next((cu["nombre"] for cu in CURSOS if cu["id"] == curso_completado), "")
        cert_docs.append({
            "user_id":           alumno_id,
            "certificate_id":    cert_id,
            "categoria":         cert["categoria"],
            "course_title":      curso_nombre,
            "issue_date":        _dt(cert["fecha"]),
            "verification_code": f"VC-{cert_id}-{alumno_id}",
        })
    db.certificates.insert_many(cert_docs)
    print(f"    certificates     : {db.certificates.count_documents({})} documentos")

    # ── 6. CONVERSACIONES ────────────────────────────────────────────────────
    # Una conversacion de muestra por cada par alumno-instructor activo
    conv_samples = [
        ("A1", "M1", "C1", "Profe, tengo duda con la leccion de gramatica.",
         datetime(2026, 4, 24, 15, 0, tzinfo=timezone.utc)),
        ("A2", "M2", "C2", "Excelente trabajo en el quiz!",
         datetime(2026, 3, 12, 10, 0, tzinfo=timezone.utc)),
        ("A3", "M3", "C3", "Cuando es la entrega del proyecto final?",
         datetime(2026, 4, 25, 9, 0, tzinfo=timezone.utc)),
    ]
    conv_ids = []
    for alumno_id, maestro_id, curso_id, last_body, sent_at in conv_samples:
        result = db.conversations.insert_one({
            "course_id":    curso_id,
            "participants": [alumno_id, maestro_id],
            "last_message": {"body": last_body, "sender_id": alumno_id, "sent_at": sent_at},
            "unread_by":    [maestro_id],
            "created_at":   datetime(2026, 4, 20, tzinfo=timezone.utc),
        })
        conv_ids.append((result.inserted_id, alumno_id, maestro_id, last_body, sent_at))
    print(f"    conversations    : {db.conversations.count_documents({})} documentos")

    # ── 7. MENSAJES ──────────────────────────────────────────────────────────
    msg_docs = []
    for conv_oid, alumno_id, maestro_id, last_body, sent_at in conv_ids:
        msg_docs.append({
            "conversation_id": conv_oid,
            "sender_id": alumno_id,
            "body": last_body,
            "attachment": None,
            "sent_at": sent_at,
            "read_at": None,
        })
    db.messages.insert_many(msg_docs)
    print(f"    messages         : {db.messages.count_documents({})} documentos")

    # ── 8. ANUNCIOS ──────────────────────────────────────────────────────────
    ann_ids = []
    anuncio_samples = [
        ("C1", "M1", "Cambio de horario — Semana del 28 de abril",
         "La clase del lunes 28 se mueve al miercoles 30 a las 10:00.", "high",
         datetime(2026, 5, 1, tzinfo=timezone.utc), 4),
        ("C2", "M2", "Material extra publicado",
         "Subi ejercicios adicionales en la seccion de recursos.", "normal", None, 3),
        ("C3", "M3", "Proyecto final: fecha limite 10 de mayo",
         "El proyecto se entrega el 10 de mayo antes de las 23:59.", "urgent",
         datetime(2026, 5, 11, tzinfo=timezone.utc), 5),
        ("C4", "M3", "Nueva leccion disponible: Testing con pytest",
         "Ya esta disponible la leccion 3.", "normal", None, 2),
        ("C5", "M2", "Quiz disponible en el campus virtual",
         "El quiz de distribucion normal ya esta activo.", "normal", None, 3),
        ("C6", "M4", "Sesion en vivo este viernes",
         "Conectate el viernes a las 16:00 para la sesion de NoSQL.", "high",
         datetime(2026, 5, 20, tzinfo=timezone.utc), 4),
        ("C7", "M1", "Ejercicios de escritura publicados",
         "Practica de writing disponible en recursos.", "normal", None, 2),
        ("C8", "M5", "Examen parcial la proxima semana",
         "El parcial de derivadas sera el miercoles a las 10:00.", "urgent",
         datetime(2026, 6, 30, tzinfo=timezone.utc), 3),
    ]
    for curso_id, maestro_id, title, body, priority, expires_at, total_enrolled in anuncio_samples:
        result = db.announcements.insert_one({
            "course_id":      curso_id,
            "instructor_id":  maestro_id,
            "title":          title,
            "body":           body,
            "priority":       priority,
            "expires_at":     expires_at,
            "created_at":     datetime(2026, 4, 24, tzinfo=timezone.utc),
            "total_enrolled": total_enrolled,
        })
        ann_ids.append(result.inserted_id)
    print(f"    announcements    : {db.announcements.count_documents({})} documentos")

    # ── 9. USER_ANNOUNCEMENTS ────────────────────────────────────────────────
    ua_docs = [
        {"user_id": "A1", "announcement_id": ann_ids[0],
         "read_at": datetime(2026, 4, 24, 10, 0, tzinfo=timezone.utc)},
        {"user_id": "A2", "announcement_id": ann_ids[1],
         "read_at": datetime(2026, 4, 20, 12, 0, tzinfo=timezone.utc)},
        {"user_id": "A1", "announcement_id": ann_ids[2],
         "read_at": datetime(2026, 4, 25, 14, 0, tzinfo=timezone.utc)},
        {"user_id": "A3", "announcement_id": ann_ids[2],
         "read_at": datetime(2026, 4, 25, 16, 0, tzinfo=timezone.utc)},
        {"user_id": "A5", "announcement_id": ann_ids[4],
         "read_at": datetime(2026, 5, 1, 9, 0, tzinfo=timezone.utc)},
    ]
    db.user_announcements.insert_many(ua_docs)
    print(f"    user_announcements: {db.user_announcements.count_documents({})} documentos")

    # ── Indices ──────────────────────────────────────────────────────────────
    db.users.create_index("email", unique=True)
    db.courses.create_index("instructor_id")
    db.courses.create_index([("is_published", 1), ("category", 1), ("avg_rating", -1)])
    db.courses.create_index([("title", "text"), ("description", "text")])
    db.enrollments.create_index([("user_id", 1), ("course_id", 1)], unique=True)
    db.enrollments.create_index([("user_id", 1), ("status", 1)])
    db.quizzes.create_index("course_id")
    db.certificates.create_index("user_id")
    db.certificates.create_index("verification_code", unique=True)
    db.conversations.create_index("participants")
    db.conversations.create_index("unread_by")
    db.conversations.create_index([("last_message.sent_at", -1)])
    db.messages.create_index([("conversation_id", 1), ("sent_at", 1)])
    db.announcements.create_index([("course_id", 1), ("created_at", -1)])
    db.announcements.create_index("expires_at", expireAfterSeconds=0)
    db.user_announcements.create_index([("user_id", 1), ("announcement_id", 1)], unique=True)
    db.user_announcements.create_index("announcement_id")

    print("  MongoDB: datos insertados correctamente.")
    client.close()


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 3 — DGRAPH
# ═══════════════════════════════════════════════════════════════════════════════

def populate_dgraph(reset=True):
    stub   = pydgraph.DgraphClientStub("localhost:9080")
    client = pydgraph.DgraphClient(stub)

    try:
        if reset:
            client.alter(pydgraph.Operation(drop_all=True))
            print("  Dgraph: base reiniciada.")

        # schema
        with open(SCHEMA_DQL, encoding="utf-8") as f:
            client.alter(pydgraph.Operation(schema=f.read()))
        print("  Dgraph: schema aplicado.")

        # ── nodos base ────────────────────────────────────────────────────────
        payload = []
        for a in ALUMNOS:
            payload.append({"uid": f"_:{a['id']}", "dgraph.type": "Alumno",
                             "id_alumno": a["id"], "nombre": a["nombre"], "genero": a["genero"]})
        for c in CURSOS:
            payload.append({"uid": f"_:{c['id']}", "dgraph.type": "Curso",
                             "id_curso": c["id"], "nombre": c["nombre"],
                             "categoria": c["categoria"], "day_of_week": c["day_of_week"],
                             "start_time": c["start_time"], "end_time": c["end_time"]})
        for m in MAESTROS:
            payload.append({"uid": f"_:{m['id']}", "dgraph.type": "Maestro",
                             "id_maestro": m["id"], "nombre": m["nombre"], "genero": m["genero"]})
        for t in TAREAS:
            payload.append({"uid": f"_:{t}", "dgraph.type": "Tarea", "id_tarea": t})
        for e in EXAMENES:
            payload.append({"uid": f"_:{e['id']}", "dgraph.type": "Examen",
                             "id_examen": e["id"], "preguntas": e["preguntas"]})
        for cert in CERTIFICADOS:
            payload.append({"uid": f"_:{cert['id']}", "dgraph.type": "Certificado",
                             "id_certificado": cert["id"], "fecha": cert["fecha"],
                             "categoria": cert["categoria"]})

        txn = client.txn()
        try:
            resp = txn.mutate(set_obj=payload, commit_now=True)
        finally:
            txn.discard()

        uids = dict(resp.uids)
        print(f"  Dgraph: {len(uids)} nodos insertados.")

        def u(k):
            return f"<{uids[k]}>"

        # ── relaciones ────────────────────────────────────────────────────────
        nq = []

        for alumno_id, curso_id, enrolled_at, status, progress, last_access, sessions_count, act_status in INSCRIPCIONES:
            nq.append(
                f'{u(alumno_id)} <inscrito_en> {u(curso_id)} '
                f'(enrolled_at="{enrolled_at}", status="{status}", '
                f'progress={progress}, last_access="{last_access}", '
                f'sessions_count={sessions_count}, activity_status="{act_status}") .'
            )

        for maestro_id, curso_id, assigned_at in IMPARTE:
            nq.append(f'{u(maestro_id)} <imparte> {u(curso_id)} (assigned_at="{assigned_at}") .')

        for curso_id, tarea_id, due_date in CONTIENE_TAREA:
            nq.append(f'{u(curso_id)} <contiene_tarea> {u(tarea_id)} (due_date="{due_date}") .')

        for i in range(1, 9):
            nq.append(f'{u(f"C{i}")} <tiene_examenes> {u(f"E{i}")} .')

        for alumno_id, tarea_id, submitted_at, status, score in ENTREGAS:
            nq.append(
                f'{u(alumno_id)} <entrega_tarea> {u(tarea_id)} '
                f'(submitted_at="{submitted_at}", status="{status}", score={score}) .'
            )

        for alumno_id, examen_id, attempt_date, score in EXAMENES_REALIZADOS:
            nq.append(
                f'{u(alumno_id)} <realiza_examen> {u(examen_id)} '
                f'(attempt_date="{attempt_date}", score={score}) .'
            )

        for maestro_id, tarea_id in ASIGNA_TAREA:
            nq.append(f"{u(maestro_id)} <asigna_tarea> {u(tarea_id)} .")

        for maestro_id, tarea_id, score in CALIFICA_TAREA:
            nq.append(f"{u(maestro_id)} <califica_tarea> {u(tarea_id)} (score={score}) .")

        for maestro_id, examen_id, score in CALIFICA_EXAMEN:
            nq.append(f"{u(maestro_id)} <califica_examen> {u(examen_id)} (score={score}) .")

        for src, dst in PREREQUISITOS:
            nq.append(f"{u(src)} <es_prerrequisito_de> {u(dst)} .")

        for alumno_id, cert_id in OBTIENE_CERTIFICADO:
            nq.append(f"{u(alumno_id)} <obtiene_certificado> {u(cert_id)} .")

        txn = client.txn()
        try:
            txn.mutate(set_nquads="\n".join(nq), commit_now=True)
        finally:
            txn.discard()

        print(f"  Dgraph: {len(nq)} relaciones insertadas.")
        print("  Dgraph: datos insertados correctamente.")

    finally:
        stub.close()


# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 4 — CASSANDRA
# ═══════════════════════════════════════════════════════════════════════════════

def _cass_ts(iso_str):
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def _parse_cql(path):
    stmts, current = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("--"):
                continue
            current.append(line)
            if stripped.endswith(";"):
                stmt = "".join(current).strip().rstrip(";")
                if not stmt.upper().startswith("USE "):
                    stmts.append(stmt)
                current = []
    return stmts


def populate_cassandra(reset=True):
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect()

    stmts = _parse_cql(SCHEMA_CQL)
    for stmt in stmts:
        if "KEYSPACE" in stmt.upper():
            session.execute(stmt)
    session.set_keyspace("vibecoders")
    for stmt in stmts:
        if "KEYSPACE" not in stmt.upper():
            session.execute(stmt)
    print("  Cassandra: keyspace y tablas creadas.")

    if reset:
        for table in ["sessions_by_student", "lesson_progress_by_student_course",
                      "quiz_attempts_by_student", "quiz_attempts_by_student_course",
                      "activity_by_student_day", "video_events_by_student",
                      "activity_by_course_day", "submissions_by_student_course",
                      "lesson_progress_by_course_lesson", "notifications_by_student"]:
            session.execute(f"TRUNCATE {table}")
        print("  Cassandra: tablas vaciadas.")

    # ── C01: sesiones de estudio ──────────────────────────────────────────────
    ins_session = session.prepare(
        "INSERT INTO sessions_by_student "
        "(student_id, session_start, session_end, course_id, device_type, session_duration) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    devices = ["desktop", "mobile", "tablet"]
    for alumno_id, curso_id, enrolled_at, _, _, last_access, sessions_count, _ in INSCRIPCIONES:
        base_ts = _cass_ts(enrolled_at)
        for i in range(min(sessions_count, 5)):
            from datetime import timedelta
            start = base_ts + timedelta(days=i * 3, hours=8)
            duration = 45 + (i * 7 % 30)
            end = start + timedelta(minutes=duration)
            session.execute(ins_session, (alumno_id, start, end, curso_id,
                                          devices[i % 3], duration * 60))
    print("  Cassandra: sessions_by_student insertado.")

    # ── C02 / C09: progreso por leccion ──────────────────────────────────────
    ins_prog_sc = session.prepare(
        "INSERT INTO lesson_progress_by_student_course "
        "(student_id, course_id, lesson_id, progress_percent, status, last_accessed_at) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    ins_prog_cl = session.prepare(
        "INSERT INTO lesson_progress_by_course_lesson "
        "(course_id, lesson_id, student_id, progress_percent, status, last_accessed_at) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    for alumno_id, curso_id, _, status, progress, last_access, _, _ in INSCRIPCIONES:
        lesson_ids = _LESSON_IDS_BY_CURSO[curso_id]
        n_total = len(lesson_ids)
        n_completed = round(progress / 100 * n_total)
        la_ts = _cass_ts(last_access)
        for idx, lesson_id in enumerate(lesson_ids):
            if idx < n_completed:
                les_pct = 100.0
                les_status = "completed"
            elif idx == n_completed and progress % (100 // n_total if n_total else 1) > 0:
                les_pct = float(progress % (100 // n_total if n_total else 1) * n_total)
                les_status = "in_progress"
            else:
                les_pct = 0.0
                les_status = "not_started"
            session.execute(ins_prog_sc, (alumno_id, curso_id, lesson_id,
                                          les_pct, les_status, la_ts))
            session.execute(ins_prog_cl, (curso_id, lesson_id, alumno_id,
                                          les_pct, les_status, la_ts))
    print("  Cassandra: lesson_progress insertado.")

    # ── C03 / C04: intentos de quiz ───────────────────────────────────────────
    ins_qa = session.prepare(
        "INSERT INTO quiz_attempts_by_student "
        "(student_id, attempt_time, quiz_id, score, duration_seconds, passed) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    ins_qa_sc = session.prepare(
        "INSERT INTO quiz_attempts_by_student_course "
        "(student_id, course_id, attempt_time, quiz_id, score, passed) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    for alumno_id, examen_id, attempt_date, score in EXAMENES_REALIZADOS:
        curso_id = _curso_by_examen[examen_id]
        ts = _cass_ts(attempt_date)
        passed = score >= 70
        session.execute(ins_qa, (alumno_id, ts, examen_id, float(score), 1800, passed))
        session.execute(ins_qa_sc, (alumno_id, curso_id, ts, examen_id, float(score), passed))
    print("  Cassandra: quiz_attempts insertado.")

    # ── C05: actividad diaria ─────────────────────────────────────────────────
    ins_act = session.prepare(
        "INSERT INTO activity_by_student_day "
        "(student_id, activity_date, event_time, event_type, course_id, lesson_id, resource_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    ins_act_c = session.prepare(
        "INSERT INTO activity_by_course_day "
        "(course_id, activity_date, event_time, student_id, event_type, lesson_id, resource_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    event_types = ["login", "lesson_view", "quiz_start", "quiz_submit", "logout"]
    for alumno_id, curso_id, enrolled_at, _, _, last_access, _, _ in INSCRIPCIONES:
        la_ts = _cass_ts(last_access)
        act_date = la_ts.date()
        lesson_ids = _LESSON_IDS_BY_CURSO[curso_id]
        from datetime import timedelta
        for i, evt in enumerate(event_types[:3]):
            evt_time = la_ts + timedelta(minutes=i * 10)
            lesson_id = lesson_ids[0] if lesson_ids else ""
            session.execute(ins_act, (alumno_id, act_date, evt_time, evt, curso_id, lesson_id, ""))
            session.execute(ins_act_c, (curso_id, act_date, evt_time, alumno_id, evt, lesson_id, ""))
    print("  Cassandra: activity insertado.")

    # ── C06: eventos de video ─────────────────────────────────────────────────
    ins_vid = session.prepare(
        "INSERT INTO video_events_by_student "
        "(student_id, event_time, video_id, event_type, watched_seconds, course_id, lesson_id) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    vid_events = ["play", "pause", "complete"]
    from datetime import timedelta
    for alumno_id, curso_id, _, _, progress, last_access, _, _ in INSCRIPCIONES:
        if progress == 0:
            continue
        la_ts = _cass_ts(last_access)
        lesson_ids = _LESSON_IDS_BY_CURSO[curso_id]
        lesson_id = lesson_ids[0] if lesson_ids else ""
        for i, evt in enumerate(vid_events):
            session.execute(ins_vid, (alumno_id, la_ts + timedelta(minutes=i * 5),
                                      lesson_id, evt, (i + 1) * 120, curso_id, lesson_id))
    print("  Cassandra: video_events insertado.")

    # ── C08: entregas de tareas ───────────────────────────────────────────────
    ins_sub = session.prepare(
        "INSERT INTO submissions_by_student_course "
        "(student_id, course_id, submitted_at, assignment_id, submission_status, grade, feedback_available) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    for alumno_id, tarea_id, submitted_at, status, score in ENTREGAS:
        curso_id = _curso_by_tarea[tarea_id]
        session.execute(ins_sub, (alumno_id, curso_id, _cass_ts(submitted_at),
                                  tarea_id, status, float(score), score > 0))
    print("  Cassandra: submissions insertado.")

    # ── C10: notificaciones ───────────────────────────────────────────────────
    ins_notif = session.prepare(
        "INSERT INTO notifications_by_student "
        "(student_id, notification_time, notification_id, notification_type, "
        "title, message, course_id, read_status) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    import uuid as _uuid
    for alumno_id, curso_id, enrolled_at, _, progress, last_access, _, _ in INSCRIPCIONES:
        la_ts = _cass_ts(last_access)
        curso_nombre = next(c["nombre"] for c in CURSOS if c["id"] == curso_id)
        session.execute(ins_notif, (
            alumno_id, la_ts, str(_uuid.uuid4()), "course_update",
            f"Nuevo contenido en {curso_nombre}",
            "Se ha publicado material nuevo en tu curso.", curso_id, False
        ))
    print("  Cassandra: notifications insertado.")

    session.shutdown()
    cluster.shutdown()
    print("  Cassandra: datos insertados correctamente.")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def populate_all(reset=True):
    print("\n[1/3] MongoDB...")
    populate_mongo(reset=reset)
    print("\n[2/3] Dgraph...")
    populate_dgraph(reset=reset)
    print("\n[3/3] Cassandra...")
    populate_cassandra(reset=reset)
    print("\nPoblacion completa.")


if __name__ == "__main__":
    populate_all(reset=True)
