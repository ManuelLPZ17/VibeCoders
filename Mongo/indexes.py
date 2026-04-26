from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["vibecoders"]

# USERS
db.users.create_index("user_id", unique=True)
db.users.create_index("email", unique=True)

# COURSES
db.courses.create_index("course_id", unique=True)
db.courses.create_index([("title", "text"), ("description", "text")])
db.courses.create_index([("is_published", 1), ("category", 1), ("avg_rating", -1)])
db.courses.create_index("instructor_id")

# ENROLLMENTS
db.enrollments.create_index([("user_id", 1), ("course_id", 1)], unique=True)
db.enrollments.create_index([("user_id", 1), ("status", 1)])

# QUIZZES
db.quizzes.create_index("quiz_id", unique=True)
db.quizzes.create_index("course_id")

# CERTIFICATES
db.certificates.create_index("user_id")
db.certificates.create_index("verification_code", unique=True)

# CONVERSATIONS
db.conversations.create_index("participants")
db.conversations.create_index("unread_by")
db.conversations.create_index([("last_message_at", -1)])

# MESSAGES
db.messages.create_index([("conversation_id", 1), ("sent_at", 1)])

# ANNOUNCEMENTS
db.announcements.create_index([("course_id", 1), ("created_at", -1)])
db.announcements.create_index("expires_at", expireAfterSeconds=0)

# USER_ANNOUNCEMENTS
db.user_announcements.create_index(
    [("user_id", 1), ("announcement_id", 1)],
    unique=True
)
db.user_announcements.create_index([("user_id", 1), ("read_at", 1)])

print("Índices creados correctamente")