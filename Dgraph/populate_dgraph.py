"""
populate_dgraph.py
Carga el schema y los datos de Dgraph leyendo los CSV de /data.
"""

import csv
import json
import os
import sys

import pydgraph

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from connect import connect_dgraph  # noqa: E402

DATA_DIR    = os.path.join(ROOT, "data")
SCHEMA_PATH = os.path.join(ROOT, "Dgraph", "schema.dql")


def _load_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def apply_schema(client):
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = f.read()
    client.alter(pydgraph.Operation(schema=schema))
    print("[Dgraph] schema aplicado")


def drop_all(client):
    client.alter(pydgraph.Operation(drop_all=True))
    print("[Dgraph] base reiniciada (drop_all)")


def insert_nodes(client):
    payload = []

    for row in _load_csv("alumnos.csv"):
        payload.append({
            "uid":         f"_:{row['id_alumno']}",
            "dgraph.type": "Alumno",
            "id_alumno":   row["id_alumno"],
            "nombre":      row["nombre"],
            "genero":      row["genero"],
        })

    for row in _load_csv("cursos.csv"):
        payload.append({
            "uid":         f"_:{row['id_curso']}",
            "dgraph.type": "Curso",
            "id_curso":    row["id_curso"],
            "nombre":      row["nombre"],
            "categoria":   row["categoria"],
            "day_of_week": row["day_of_week"],
            "start_time":  row["start_time"],
            "end_time":    row["end_time"],
        })

    for row in _load_csv("maestros.csv"):
        payload.append({
            "uid":          f"_:{row['id_maestro']}",
            "dgraph.type":  "Maestro",
            "id_maestro":   row["id_maestro"],
            "nombre":       row["nombre"],
            "genero":       row["genero"],
        })

    for row in _load_csv("tareas.csv"):
        payload.append({
            "uid":         f"_:{row['id_tarea']}",
            "dgraph.type": "Tarea",
            "id_tarea":    row["id_tarea"],
        })

    for row in _load_csv("examenes.csv"):
        raw = row["preguntas"]
        preguntas = [p.strip() for p in raw.split(";")] if ";" in raw else [raw]
        payload.append({
            "uid":         f"_:{row['id_examen']}",
            "dgraph.type": "Examen",
            "id_examen":   row["id_examen"],
            "preguntas":   preguntas,
        })

    for row in _load_csv("certificados.csv"):
        payload.append({
            "uid":            f"_:{row['id_certificado']}",
            "dgraph.type":    "Certificado",
            "id_certificado": row["id_certificado"],
            "fecha":          row["fecha"],
            "categoria":      row["categoria"],
        })

    txn = client.txn()
    try:
        resp = txn.mutate(set_obj=payload, commit_now=True)
    finally:
        txn.discard()

    uids = dict(resp.uids)
    print(f"[Dgraph] insertados {len(uids)} nodos base")
    return uids


def insert_relations(client, uids):
    def u(k):
        return f"<{uids[k]}>"

    nq = []

    # ---- RF01 / RF08 / RF10 — inscripciones --------------------------
    inscripciones = [
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
    for a, c, enrolled, status, progress, la, sessions, act_status in inscripciones:
        nq.append(
            f'{u(a)} <inscrito_en> {u(c)} '
            f'(enrolled_at="{enrolled}", status="{status}", '
            f'progress={progress}, last_access="{la}", '
            f'sessions_count={sessions}, activity_status="{act_status}") .'
        )

    # ---- RF02 — imparte ----------------------------------------------
    imparte = [
        ("M1", "C1", "2026-01-05T00:00:00Z"),
        ("M1", "C7", "2026-01-05T00:00:00Z"),
        ("M2", "C2", "2026-01-05T00:00:00Z"),
        ("M2", "C5", "2026-01-06T00:00:00Z"),
        ("M3", "C3", "2026-01-06T00:00:00Z"),
        ("M3", "C4", "2026-01-06T00:00:00Z"),
        ("M4", "C6", "2026-01-07T00:00:00Z"),
        ("M5", "C8", "2026-01-07T00:00:00Z"),
    ]
    for m, c, d in imparte:
        nq.append(f'{u(m)} <imparte> {u(c)} (assigned_at="{d}") .')

    # ---- RF05 — contiene_tarea ---------------------------------------
    contiene = [
        ("C1", "T1", "2026-05-01T00:00:00Z"),
        ("C2", "T2", "2026-05-10T00:00:00Z"),
        ("C3", "T3", "2026-06-01T00:00:00Z"),
        ("C4", "T4", "2026-06-15T00:00:00Z"),
        ("C5", "T5", "2026-05-20T00:00:00Z"),
        ("C6", "T6", "2026-06-05T00:00:00Z"),
        ("C7", "T7", "2026-05-15T00:00:00Z"),
        ("C8", "T8", "2026-06-20T00:00:00Z"),
    ]
    for c, t, due in contiene:
        nq.append(f'{u(c)} <contiene_tarea> {u(t)} (due_date="{due}") .')

    # ---- tiene_examenes ----------------------------------------------
    for i in range(1, 9):
        nq.append(f'{u(f"C{i}")} <tiene_examenes> {u(f"E{i}")} .')

    # ---- RF03 — entregas de tarea ------------------------------------
    entregas = [
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
    for a, t, when, status, score in entregas:
        nq.append(
            f'{u(a)} <entrega_tarea> {u(t)} '
            f'(submitted_at="{when}", status="{status}", score={score}) .'
        )

    # ---- RF04 — examenes realizados ----------------------------------
    examenes = [
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
    for a, e, when, score in examenes:
        nq.append(
            f'{u(a)} <realiza_examen> {u(e)} '
            f'(attempt_date="{when}", score={score}) .'
        )

    # ---- asigna_tarea / califica_tarea / califica_examen -------------
    asigna = [
        ("M1", "T1"), ("M1", "T7"),
        ("M2", "T2"), ("M2", "T5"),
        ("M3", "T3"), ("M3", "T4"),
        ("M4", "T6"), ("M5", "T8"),
    ]
    for m, t in asigna:
        nq.append(f"{u(m)} <asigna_tarea> {u(t)} .")

    califica_t = [
        ("M1", "T1", 90), ("M1", "T7", 82),
        ("M2", "T2", 80), ("M2", "T5", 91),
        ("M3", "T3", 70), ("M3", "T4", 60),
        ("M4", "T6", 75), ("M5", "T8", 88),
    ]
    for m, t, s in califica_t:
        nq.append(f"{u(m)} <califica_tarea> {u(t)} (score={s}) .")

    califica_e = [
        ("M1", "E1", 85), ("M1", "E7", 82),
        ("M2", "E2", 60), ("M2", "E5", 90),
        ("M3", "E3", 95), ("M3", "E4", 50),
        ("M4", "E6", 75), ("M5", "E8", 88),
    ]
    for m, e, s in califica_e:
        nq.append(f"{u(m)} <califica_examen> {u(e)} (score={s}) .")

    # ---- RF09 — prerrequisitos ---------------------------------------
    prereq = [
        ("C1", "C7"),
        ("C2", "C5"),
        ("C2", "C8"),
        ("C3", "C4"),
        ("C5", "C8"),
    ]
    for src, dst in prereq:
        nq.append(f"{u(src)} <es_prerrequisito_de> {u(dst)} .")

    # ---- certificados ------------------------------------------------
    obtiene = [
        ("A5",  "CERT1"),
        ("A2",  "CERT2"),
        ("A4",  "CERT3"),
        ("A9",  "CERT4"),
        ("A8",  "CERT5"),
        ("A13", "CERT6"),
        ("A1",  "CERT7"),
    ]
    for a, cert in obtiene:
        nq.append(f"{u(a)} <obtiene_certificado> {u(cert)} .")

    nquads = "\n".join(nq)
    txn = client.txn()
    try:
        txn.mutate(set_nquads=nquads, commit_now=True)
    finally:
        txn.discard()
    print(f"[Dgraph] insertadas {len(nq)} relaciones (RF01-RF10)")


def verify(client):
    q = """
    {
      alumnos(func: type(Alumno))           { uid id_alumno  nombre }
      cursos(func: type(Curso))             { uid id_curso   nombre day_of_week }
      maestros(func: type(Maestro))         { uid id_maestro nombre }
      tareas(func: type(Tarea))             { uid id_tarea }
      examenes(func: type(Examen))          { uid id_examen }
      certificados(func: type(Certificado)) { uid id_certificado }
    }
    """
    res = client.txn(read_only=True).query(q)
    data = json.loads(res.json)
    print("[Dgraph] verificacion:")
    for k, v in data.items():
        print(f"   {k}: {len(v)}")
    return data


def populate_dgraph(reset=True):
    stub, client = connect_dgraph()
    try:
        if reset:
            drop_all(client)
        apply_schema(client)
        uids = insert_nodes(client)
        insert_relations(client, uids)
        verify(client)
        return uids
    finally:
        stub.close()


if __name__ == "__main__":
    populate_dgraph(reset=True)