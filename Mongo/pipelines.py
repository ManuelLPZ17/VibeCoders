from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["vibecoders"]

# RF03 - progreso
def progreso_usuario(user_id, course_id):
    pipeline = [
        {"$match": {"user_id": user_id, "course_id": course_id}},
        {
            "$lookup": {
                "from": "courses",
                "localField": "course_id",
                "foreignField": "course_id",
                "as": "course"
            }
        },
        {"$unwind": "$course"},
        {
            "$project": {
                "progress_percentage": 1,
                "completed": {"$size": "$completed_lessons"},
                "total": {"$size": "$course.lessons"}
            }
        }
    ]
    return list(db.enrollments.aggregate(pipeline))


# RF06 - inbox
def inbox(user_id):
    pipeline = [
        {"$match": {"participants": user_id}},
        {
            "$addFields": {
                "has_unread": {"$in": [user_id, "$unread_by"]}
            }
        },
        {
            "$sort": {"has_unread": -1, "last_message_at": -1}
        }
    ]
    return list(db.conversations.aggregate(pipeline))


# RF10 - anuncios no leídos
def anuncios_no_leidos(user_id):
    pipeline = [
        {
            "$lookup": {
                "from": "user_announcements",
                "let": {"ann_id": "$announcement_id"},
                "pipeline": [
                    {"$match": {"user_id": user_id}},
                    {
                        "$match": {
                            "$expr": {
                                "$eq": ["$announcement_id", "$$ann_id"]
                            }
                        }
                    }
                ],
                "as": "read_info"
            }
        },
        {
            "$match": {"read_info": {"$size": 0}}
        }
    ]
    return list(db.announcements.aggregate(pipeline))
