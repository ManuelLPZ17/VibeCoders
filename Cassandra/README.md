# Cassandra

Cassandra se usa en VibeCoders para guardar eventos e historiales de alto volumen:
sesiones de estudio, avance por leccion, intentos de quizzes, actividad diaria,
eventos de video, entregas y notificaciones.

## Requerimientos funcionales

| RF | Tabla | Consulta |
| --- | --- | --- |
| RF01 | `sessions_by_student` | Sesiones recientes de un estudiante |
| RF02 | `lesson_progress_by_student_course` | Avance de un estudiante dentro de un curso |
| RF03 | `quiz_attempts_by_student` | Intentos recientes de quizzes por estudiante |
| RF04 | `quiz_attempts_by_student_course` | Intentos de quizzes por estudiante y curso |
| RF05 | `activity_by_student_day` | Actividad diaria de un estudiante |
| RF06 | `video_events_by_student` | Eventos de video por estudiante |
| RF07 | `activity_by_course_day` | Actividad reciente dentro de un curso en una fecha |
| RF08 | `submissions_by_student_course` | Entregas por estudiante y curso |
| RF09 | `lesson_progress_by_course_lesson` | Estudiantes que avanzaron una leccion |
| RF10 | `notifications_by_student` | Notificaciones recientes por estudiante |

## Levantar Cassandra con Docker

```bash
docker run --name cassandra -p 9042:9042 -d cassandra:4.1
```

Cassandra puede tardar algunos segundos en iniciar completamente despues de levantar el contenedor.

Si el contenedor ya existe pero esta detenido:

```bash
docker start cassandra
```

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Poblar datos

Desde el menu principal:

```bash
python main.py
```

Seleccionar:

```text
P
```

Tambien se puede poblar solo Cassandra:

```bash
python Cassandra/populate_cassandra.py
```

El poblado aplica `Cassandra/schema.cql`, limpia las tablas si se ejecuta con
`reset=True` y carga datos de prueba consistentes con `Cassandra/queries.cql`.

## Ejecutar las 10 queries

```bash
python main.py
```

Seleccionar:

```text
2
```

Luego elegir cualquiera de las opciones RF01 a RF10 del submenu de Cassandra.
Cada opcion ejecuta una consulta real usando las llaves de particion correctas y
muestra resultados visibles en consola.
