CREATE KEYSPACE IF NOT EXISTS vibecoders
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

USE vibecoders;

-- C01: ¿Cuáles han sido las sesiones de estudio más recientes de un estudiante y cuánto tiempo dedicó a cada una?
CREATE TABLE IF NOT EXISTS sessions_by_student (
    student_id text,
    session_start timestamp,
    session_end timestamp,
    course_id text,
    device_type text,
    session_duration int,
    PRIMARY KEY (student_id, session_start)
) WITH CLUSTERING ORDER BY (session_start DESC);

-- C02: ¿Qué lecciones de un curso ha completado o tiene en progreso un estudiante?
CREATE TABLE IF NOT EXISTS lesson_progress_by_student_course (
    student_id text,
    course_id text,
    lesson_id text,
    progress_percent decimal,
    status text,
    last_accessed_at timestamp,
    PRIMARY KEY ((student_id, course_id), lesson_id)
);

-- C03: ¿Qué cuestionarios ha presentado recientemente un estudiante y qué resultado obtuvo en cada uno?
CREATE TABLE IF NOT EXISTS quiz_attempts_by_student (
    student_id text,
    attempt_time timestamp,
    quiz_id text,
    score decimal,
    duration_seconds int,
    passed boolean,
    PRIMARY KEY (student_id, attempt_time)
) WITH CLUSTERING ORDER BY (attempt_time DESC);

-- C04: ¿Qué cuestionarios ha presentado un estudiante dentro de un curso específico y qué resultado obtuvo en cada uno?
CREATE TABLE IF NOT EXISTS quiz_attempts_by_student_course (
    student_id text,
    course_id text,
    attempt_time timestamp,
    quiz_id text,
    score decimal,
    passed boolean,
    PRIMARY KEY ((student_id, course_id), attempt_time)
) WITH CLUSTERING ORDER BY (attempt_time DESC);

-- C05: ¿Qué acciones realizó un estudiante dentro de la plataforma en un día determinado?
CREATE TABLE IF NOT EXISTS activity_by_student_day (
    student_id text,
    activity_date date,
    event_time timestamp,
    event_type text,
    course_id text,
    lesson_id text,
    resource_id text,
    PRIMARY KEY ((student_id, activity_date), event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- C06: ¿Qué actividad reciente ha tenido un estudiante con los videos educativos de la plataforma?
CREATE TABLE IF NOT EXISTS video_events_by_student (
    student_id text,
    event_time timestamp,
    video_id text,
    event_type text,
    watched_seconds int,
    course_id text,
    lesson_id text,
    PRIMARY KEY (student_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- C07: ¿Qué actividad ocurrió dentro de un curso en un día determinado y qué estudiantes participaron?
CREATE TABLE IF NOT EXISTS activity_by_course_day (
    course_id text,
    activity_date date,
    event_time timestamp,
    student_id text,
    event_type text,
    lesson_id text,
    resource_id text,
    PRIMARY KEY ((course_id, activity_date), event_time, student_id)
) WITH CLUSTERING ORDER BY (event_time DESC, student_id ASC);

-- C08: ¿Qué tareas ha entregado un estudiante dentro de un curso y cuál es el estado de cada entrega?
CREATE TABLE IF NOT EXISTS submissions_by_student_course (
    student_id text,
    course_id text,
    submitted_at timestamp,
    assignment_id text,
    submission_status text,
    grade decimal,
    feedback_available boolean,
    PRIMARY KEY ((student_id, course_id), submitted_at, assignment_id)
) WITH CLUSTERING ORDER BY (submitted_at DESC, assignment_id ASC);

-- C09: ¿Qué estudiantes han avanzado o completado una lección específica dentro de un curso?
CREATE TABLE IF NOT EXISTS lesson_progress_by_course_lesson (
    course_id text,
    lesson_id text,
    student_id text,
    progress_percent decimal,
    status text,
    last_accessed_at timestamp,
    PRIMARY KEY ((course_id, lesson_id), student_id)
);

-- C10: ¿Qué notificaciones ha recibido recientemente un estudiante y qué tipo de aviso representa cada una?
CREATE TABLE IF NOT EXISTS notifications_by_student (
    student_id text,
    notification_time timestamp,
    notification_id text,
    notification_type text,
    title text,
    message text,
    course_id text,
    read_status boolean,
    PRIMARY KEY (student_id, notification_time, notification_id)
) WITH CLUSTERING ORDER BY (notification_time DESC, notification_id ASC);
