from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["vibecoders"]

# USERS — RF05
# email único para login y garantía de unicidad de cuenta
db.users.create_index("email", unique=True)

# COURSES — RF01, RF02, RF04
# acceso directo al curso por instructor
db.courses.create_index("instructor_id")
# catálogo por categoría ordenado por rating — cubre el 90% de queries del catálogo
db.courses.create_index([("is_published", 1), ("category", 1), ("avg_rating", -1)])
# búsqueda por palabras clave con scoring de relevancia
db.courses.create_index([("title", "text"), ("description", "text")])

# ENROLLMENTS — RF03, RF09
# un estudiante solo puede inscribirse una vez por curso + recuperación directa del progreso
db.enrollments.create_index([("user_id", 1), ("course_id", 1)], unique=True)
# historial filtrado por estado (in_progress, completed, abandoned)
db.enrollments.create_index([("user_id", 1), ("status", 1)])

# QUIZZES — RF07
# listar todos los quizzes de un curso
db.quizzes.create_index("course_id")

# CERTIFICATES — RF08
# listar todos los certificados del usuario
db.certificates.create_index("user_id")
# validación externa del certificado sin autenticación
db.certificates.create_index("verification_code", unique=True)

# CONVERSATIONS — RF06
# un hilo por par de usuarios — busca conversación con $all en O(log n)
db.conversations.create_index("participants", unique=True)
# inbox de no leídos sin collection scan
db.conversations.create_index("unread_by")
# inbox ordenado por actividad reciente
db.conversations.create_index([("last_message.sent_at", -1)])

# MESSAGES — RF06
# historial del hilo en orden cronológico — consulta más frecuente del sistema de mensajería
db.messages.create_index([("conversation_id", 1), ("sent_at", 1)])

# ANNOUNCEMENTS — RF10
# anuncios de un curso ordenados por recencia
db.announcements.create_index([("course_id", 1), ("created_at", -1)])
# auto-eliminación de documentos vencidos sin mantenimiento manual
db.announcements.create_index("expires_at", expireAfterSeconds=0)

# USER_ANNOUNCEMENTS — RF10
# evita duplicados de lectura + recuperación directa de si un usuario leyó un anuncio
db.user_announcements.create_index(
    [("user_id", 1), ("announcement_id", 1)],
    unique=True
)
# reporte de engagement: cuántos usuarios leyeron un anuncio
db.user_announcements.create_index("announcement_id")

print("Índices creados correctamente")


