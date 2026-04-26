USE vibecoders;

-- C01: ¿Cuáles han sido las sesiones de estudio más recientes de un estudiante y cuánto tiempo dedicó a cada una?
SELECT student_id, session_start, session_end, course_id, device_type, session_duration
FROM sessions_by_student
WHERE student_id = 'U001'
LIMIT 10;

-- C02: ¿Qué lecciones de un curso ha completado o tiene en progreso un estudiante?
SELECT lesson_id, progress_percent, status, last_accessed_at
FROM lesson_progress_by_student_course
WHERE student_id = 'U001'
AND course_id = 'C001';

-- C03: ¿Qué cuestionarios ha presentado recientemente un estudiante y qué resultado obtuvo en cada uno?
SELECT quiz_id, attempt_time, score, duration_seconds, passed
FROM quiz_attempts_by_student
WHERE student_id = 'U001'
LIMIT 10;

-- C04: ¿Qué cuestionarios ha presentado un estudiante dentro de un curso específico y qué resultado obtuvo en cada uno?
SELECT quiz_id, attempt_time, score, passed
FROM quiz_attempts_by_student_course
WHERE student_id = 'U001'
AND course_id = 'C001'
LIMIT 10;

-- C05: ¿Qué acciones realizó un estudiante dentro de la plataforma en un día determinado?
SELECT event_time, event_type, course_id, lesson_id, resource_id
FROM activity_by_student_day
WHERE student_id = 'U001'
AND activity_date = '2026-04-25'
LIMIT 20;

-- C06: ¿Qué actividad reciente ha tenido un estudiante con los videos educativos de la plataforma?
SELECT event_time, video_id, event_type, watched_seconds, course_id, lesson_id
FROM video_events_by_student
WHERE student_id = 'U001'
LIMIT 20;

-- C07: ¿Qué actividad ocurrió dentro de un curso en un día determinado y qué estudiantes participaron?
SELECT event_time, student_id, event_type, lesson_id, resource_id
FROM activity_by_course_day
WHERE course_id = 'C001'
AND activity_date = '2026-04-25'
LIMIT 20;

-- C08: ¿Qué tareas ha entregado un estudiante dentro de un curso y cuál es el estado de cada entrega?
SELECT submitted_at, assignment_id, submission_status, grade, feedback_available
FROM submissions_by_student_course
WHERE student_id = 'U001'
AND course_id = 'C001'
LIMIT 20;

-- C09: ¿Qué estudiantes han avanzado o completado una lección específica dentro de un curso?
SELECT student_id, progress_percent, status, last_accessed_at
FROM lesson_progress_by_course_lesson
WHERE course_id = 'C001'
AND lesson_id = 'L001';

-- C10: ¿Qué notificaciones ha recibido recientemente un estudiante y qué tipo de aviso representa cada una?
SELECT notification_time, notification_id, notification_type, title, message, course_id, read_status
FROM notifications_by_student
WHERE student_id = 'U001'
LIMIT 10;
