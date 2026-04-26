# MongoDB Data Population Script for VibeCoders
# 1. Crear usuarios (users)
# - Insertar estudiantes e instructores
# - Campos: user_id, username, email, password, role, created_at

# 2. Crear cursos (courses)
# - Insertar cursos con instructor_id
# - Agregar lessons con attachments

# 3. Crear inscripciones (enrollments)
# - Relacionar user_id con course_id
# - Agregar progreso y estado (in_progress, completed)

# 4. Crear quizzes (quizzes)
# - Asociar a course_id
# - Agregar preguntas

# 5. Crear certificados (certificates)
# - Solo para usuarios que completaron cursos

# 6. Crear conversaciones (conversations)
# - Entre estudiante e instructor
# - Guardar participants, last_message

# 7. Crear mensajes (messages)
# - Asociados a conversation_id
# - Simular leídos y no leídos

# 8. Crear anuncios (announcements)
# - Asociados a course_id
# - Con expires_at

# 9. Crear user_announcements
# - Registrar qué usuario leyó qué anuncio

# 10. Verificar datos
# - Que existan referencias correctas

# Cassandra Data Population Script for VibeCoders
# 1. Insertar sesiones de estudio en sessions_by_student
# - Campos: student_id, session_start, session_end, course_id, device_type, session_duration.
# - Uso: consultar las sesiones recientes de un estudiante.

# 2. Insertar progreso por lección en lesson_progress_by_student_course
# - Campos: student_id, course_id, lesson_id, progress_percent, status, last_accessed_at.
# - Uso: consultar qué lecciones de un curso ha completado o tiene en progreso un estudiante.

# 3. Insertar cuestionarios presentados por estudiante en quiz_attempts_by_student
# - Campos: student_id, attempt_time, quiz_id, score, duration_seconds, passed.
# - Uso: consultar los cuestionarios recientes presentados por un estudiante.

# 4. Insertar cuestionarios presentados por estudiante y curso en quiz_attempts_by_student_course
# - Campos: student_id, course_id, attempt_time, quiz_id, score, passed.
# - Uso: consultar los cuestionarios presentados por un estudiante dentro de un curso específico.

# 5. Insertar actividad diaria por estudiante en activity_by_student_day
# - Campos: student_id, activity_date, event_time, event_type, course_id, lesson_id, resource_id.
# - Uso: consultar las acciones realizadas por un estudiante en un día específico.

# 6. Insertar eventos de video por estudiante en video_events_by_student
# - Campos: student_id, event_time, video_id, event_type, watched_seconds, course_id, lesson_id.
# - Uso: consultar la actividad reciente de un estudiante con videos educativos.

# 7. Insertar actividad diaria por curso en activity_by_course_day
# - Campos: course_id, activity_date, event_time, student_id, event_type, lesson_id, resource_id.
# - Uso: consultar la actividad ocurrida dentro de un curso en un día específico.

# 8. Insertar entregas de tareas en submissions_by_student_course
# - Campos: student_id, course_id, submitted_at, assignment_id, submission_status, grade, feedback_available.
# - Uso: consultar las tareas entregadas por un estudiante dentro de un curso.

# 9. Insertar progreso por curso y lección en lesson_progress_by_course_lesson
# - Campos: course_id, lesson_id, student_id, progress_percent, status, last_accessed_at.
# - Uso: consultar qué estudiantes han avanzado o completado una lección específica.

# 10. Insertar notificaciones por estudiante en notifications_by_student
# - Campos: student_id, notification_time, notification_id, notification_type, title, message, course_id, read_status.
# - Uso: consultar las notificaciones recientes recibidas por un estudiante.
