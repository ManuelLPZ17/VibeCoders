"""
queries_dgraph.py
Las 10 consultas de Dgraph (RF01..RF10), ejecutables desde terminal.
Cada funcion devuelve el dict ya parseado y, si se ejecuta directamente,
imprime el resultado en JSON.

Uso desde el menu principal:
    from Dgraph.queries_dgraph import run_query
    run_query("14", client, alumno="Carlos Lopez")
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from connect import connect_dgraph  # noqa: E402


def _q(client, query, variables=None):
    txn = client.txn(read_only=True)
    try:
        if variables:
            res = txn.query(query, variables=variables)
        else:
            res = txn.query(query)
        return json.loads(res.json)
    finally:
        txn.discard()


# ---------------------------------------------------------------------------
# RF01 - cursos en los que esta inscrito un alumno + estado
# ---------------------------------------------------------------------------
def q14_inscripciones(client, alumno="Carlos Lopez"):
    q = """
    query q($n: string) {
      resultado(func: eq(nombre, $n)) @filter(type(Alumno)) {
        nombre
        inscrito_en @facets(enrolled_at, status) { nombre }
      }
    }"""
    return _q(client, q, {"$n": alumno})


# RF02 - maestros y cursos que imparten + assigned_at
def q15_imparte(client):
    q = """
    {
      maestros(func: type(Maestro)) {
        nombre
        imparte @facets(assigned_at) { nombre }
      }
    }"""
    return _q(client, q)


# RF05 - tareas de un curso con due_date
def q16_tareas_curso(client, curso="Programacion Web"):
    q = """
    query q($c: string) {
      resultado(func: eq(nombre, $c)) @filter(type(Curso)) {
        nombre
        contiene_tarea @facets(due_date) { id_tarea }
      }
    }"""
    return _q(client, q, {"$c": curso})


# RF03 - tareas entregadas por un alumno + score
def q17_entregas(client, alumno="Carlos Lopez"):
    q = """
    query q($n: string) {
      resultado(func: eq(nombre, $n)) @filter(type(Alumno)) {
        nombre
        entrega_tarea @facets(submitted_at, status, score) { id_tarea }
      }
    }"""
    return _q(client, q, {"$n": alumno})


# RF04 - examenes realizados por un alumno + resultado
def q18_examenes(client, alumno="Carlos Lopez"):
    q = """
    query q($n: string) {
      resultado(func: eq(nombre, $n)) @filter(type(Alumno)) {
        nombre
        realiza_examen @facets(attempt_date, score) { id_examen preguntas }
      }
    }"""
    return _q(client, q, {"$n": alumno})


# RF06 - calificaciones (tareas + examenes) de un alumno
def q19_calificaciones(client, alumno="Carlos Lopez"):
    q = """
    query q($n: string) {
      resultado(func: eq(nombre, $n)) @filter(type(Alumno)) {
        nombre
        entrega_tarea  @facets(score) { id_tarea }
        realiza_examen @facets(score) { id_examen }
      }
    }"""
    return _q(client, q, {"$n": alumno})


# RF07 - horario de todos los cursos
def q20_horarios(client):
    q = """
    {
      cursos(func: type(Curso), orderasc: day_of_week) {
        nombre day_of_week start_time end_time
      }
    }"""
    return _q(client, q)


# RF08 - actividad (last_access) por alumno y curso
def q21_actividad(client):
    q = """
    {
      alumnos(func: type(Alumno)) {
        nombre
        inscrito_en @facets(last_access, status) { nombre }
      }
    }"""
    return _q(client, q)


# RF09 - cadena de prerrequisitos de un curso
def q22_prerrequisitos(client, curso="Programacion Avanzada"):
    q = """
    query q($c: string) {
      resultado(func: eq(nombre, $c)) @filter(type(Curso)) {
        nombre
        ~es_prerrequisito_de {
          nombre
          ~es_prerrequisito_de { nombre }
        }
      }
    }"""
    return _q(client, q, {"$c": curso})


# RF10 - progreso porcentual por alumno
def q23_progreso(client):
    q = """
    {
      alumnos(func: type(Alumno)) {
        nombre
        inscrito_en @facets(progress, last_access) { nombre }
      }
    }"""
    return _q(client, q)


# ---------------------------------------------------------------------------
# Dispatcher para el menu principal
# ---------------------------------------------------------------------------
QUERIES = {
    "14": ("Cursos en que esta inscrito un alumno",            q14_inscripciones, ["alumno"]),
    "15": ("Maestros y cursos que imparten (assigned_at)",     q15_imparte,        []),
    "16": ("Tareas de un curso con fecha limite",              q16_tareas_curso,   ["curso"]),
    "17": ("Tareas entregadas por un alumno con calificacion", q17_entregas,       ["alumno"]),
    "18": ("Examenes realizados por un alumno y resultado",    q18_examenes,       ["alumno"]),
    "19": ("Calificaciones (tareas + examenes) de un alumno",  q19_calificaciones, ["alumno"]),
    "20": ("Horario de todos los cursos",                      q20_horarios,       []),
    "21": ("Nivel de actividad de los alumnos",                q21_actividad,      []),
    "22": ("Cadena de prerrequisitos de un curso",             q22_prerrequisitos, ["curso"]),
    "23": ("Progreso porcentual por alumno",                   q23_progreso,       []),
}


def run_query(option, client):
    desc, fn, params = QUERIES[option]
    print(f"\n>> {desc}")
    kwargs = {}
    for p in params:
        val = input(f"   {p}: ").strip()
        if val:
            kwargs[p] = val
    res = fn(client, **kwargs)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


# ---------------------------------------------------------------------------
# Standalone: corre todas las queries en secuencia (smoke test)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    stub, client = connect_dgraph()
    try:
        for opt, (desc, fn, params) in QUERIES.items():
            print(f"\n========== {opt} :: {desc} ==========")
            print(json.dumps(fn(client), indent=2, ensure_ascii=False))
    finally:
        stub.close()
