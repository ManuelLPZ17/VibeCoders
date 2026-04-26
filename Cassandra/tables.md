# Modelo de Datos — Cassandra

## sessions_by_student

{ student_id: TEXT, session_start: TIMESTAMP, session_end: TIMESTAMP, course_id: TEXT, device_type: TEXT, session_duration: INT }

Consulta que resuelve: ¿Cuáles han sido las sesiones de estudio más recientes de un estudiante y cuánto tiempo dedicó a cada una?

Clave primaria:  
PK: student_id  
CK: session_start  

---

## lesson_progress_by_student_course

{ student_id: TEXT, course_id: TEXT, lesson_id: TEXT, progress_percent: DECIMAL, status: TEXT, last_accessed_at: TIMESTAMP }

Consulta que resuelve: ¿Qué lecciones de un curso ha completado o tiene en progreso un estudiante?

Clave primaria:  
PK: student_id, course_id  
CK: lesson_id  

---

## quiz_attempts_by_student

{ student_id: TEXT, attempt_time: TIMESTAMP, quiz_id: TEXT, score: DECIMAL, duration_seconds: INT, passed: BOOLEAN }

Consulta que resuelve: ¿Qué cuestionarios ha presentado recientemente un estudiante y qué resultado obtuvo en cada uno?

Clave primaria:  
PK: student_id  
CK: attempt_time  

---

## quiz_attempts_by_student_course

{ student_id: TEXT, course_id: TEXT, attempt_time: TIMESTAMP, quiz_id: TEXT, score: DECIMAL, passed: BOOLEAN }

Consulta que resuelve: ¿Qué cuestionarios ha presentado un estudiante dentro de un curso específico y qué resultado obtuvo en cada uno?

Clave primaria:  
PK: student_id, course_id  
CK: attempt_time  

---

## activity_by_student_day

{ student_id: TEXT, activity_date: DATE, event_time: TIMESTAMP, event_type: TEXT, course_id: TEXT, lesson_id: TEXT, resource_id: TEXT }

Consulta que resuelve: ¿Qué acciones realizó un estudiante dentro de la plataforma en un día determinado?

Clave primaria:  
PK: student_id, activity_date  
CK: event_time  

---

## video_events_by_student

{ student_id: TEXT, event_time: TIMESTAMP, video_id: TEXT, event_type: TEXT, watched_seconds: INT, course_id: TEXT, lesson_id: TEXT }

Consulta que resuelve: ¿Qué actividad reciente ha tenido un estudiante con los videos educativos de la plataforma?

Clave primaria:  
PK: student_id  
CK: event_time  

---

## activity_by_course_day

{ course_id: TEXT, activity_date: DATE, event_time: TIMESTAMP, student_id: TEXT, event_type: TEXT, lesson_id: TEXT, resource_id: TEXT }

Consulta que resuelve: ¿Qué actividad ocurrió dentro de un curso en un día determinado y qué estudiantes participaron?

Clave primaria:  
PK: course_id, activity_date  
CK: event_time, student_id  

---

## submissions_by_student_course

{ student_id: TEXT, course_id: TEXT, submitted_at: TIMESTAMP, assignment_id: TEXT, submission_status: TEXT, grade: DECIMAL, feedback_available: BOOLEAN }

Consulta que resuelve: ¿Qué tareas ha entregado un estudiante dentro de un curso y cuál es el estado de cada entrega?

Clave primaria:  
PK: student_id, course_id  
CK: submitted_at, assignment_id  

---

## lesson_progress_by_course_lesson

{ course_id: TEXT, lesson_id: TEXT, student_id: TEXT, progress_percent: DECIMAL, status: TEXT, last_accessed_at: TIMESTAMP }

Consulta que resuelve: ¿Qué estudiantes han avanzado o completado una lección específica dentro de un curso?

Clave primaria:  
PK: course_id, lesson_id  
CK: student_id  

---

## notifications_by_student

{ student_id: TEXT, notification_time: TIMESTAMP, notification_id: TEXT, notification_type: TEXT, title: TEXT, message: TEXT, course_id: TEXT, read_status: BOOLEAN }

Consulta que resuelve: ¿Qué notificaciones ha recibido recientemente un estudiante y qué tipo de aviso representa cada una?

Clave primaria:  
PK: student_id  
CK: notification_time, notification_id  
