USE vibecoders;

-- RF01: Ver sesiones de estudio recientes por estudiante
SELECT student_id, session_start, session_end, course_id, device_type, session_duration
FROM sessions_by_student
WHERE student_id = 'U001'
LIMIT 10;

-- RF02: Ver avance por leccion de un estudiante en un curso
SELECT lesson_id, progress_percent, status, last_accessed_at
FROM lesson_progress_by_student_course
WHERE student_id = 'U001'
AND course_id = 'C001';

-- RF03: Ver intentos recientes de quizzes por estudiante
SELECT quiz_id, attempt_time, score, duration_seconds, passed
FROM quiz_attempts_by_student
WHERE student_id = 'U001'
LIMIT 10;

-- RF04: Ver intentos de quizzes por estudiante y curso
SELECT quiz_id, attempt_time, score, passed
FROM quiz_attempts_by_student_course
WHERE student_id = 'U001'
AND course_id = 'C001'
LIMIT 10;

-- RF05: Ver actividad diaria de un estudiante
SELECT event_time, event_type, course_id, lesson_id, resource_id
FROM activity_by_student_day
WHERE student_id = 'U001'
AND activity_date = '2026-04-25'
LIMIT 20;

-- RF06: Ver eventos de video por estudiante
SELECT event_time, video_id, event_type, watched_seconds, course_id, lesson_id
FROM video_events_by_student
WHERE student_id = 'U001'
LIMIT 20;

-- RF07: Ver actividad reciente dentro de un curso
SELECT event_time, student_id, event_type, lesson_id, resource_id
FROM activity_by_course_day
WHERE course_id = 'C001'
AND activity_date = '2026-04-25'
LIMIT 20;

-- RF08: Ver entregas de tareas por estudiante y curso
SELECT submitted_at, assignment_id, submission_status, grade, feedback_available
FROM submissions_by_student_course
WHERE student_id = 'U001'
AND course_id = 'C001'
LIMIT 20;

-- RF09: Ver progreso de estudiantes por curso y leccion
SELECT student_id, progress_percent, status, last_accessed_at
FROM lesson_progress_by_course_lesson
WHERE course_id = 'C001'
AND lesson_id = 'L001';

-- RF10: Ver notificaciones recientes por estudiante
SELECT notification_time, notification_id, notification_type, title, message, course_id, read_status
FROM notifications_by_student
WHERE student_id = 'U001'
LIMIT 10;
