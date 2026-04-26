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