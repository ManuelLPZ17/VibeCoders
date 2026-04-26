# Modelo de Datos — MongoDB

## users
{
  user_id: String,
  username: String,
  email: String,
  hashed_password: String,
  role: "student" | "instructor",
  created_at: Date
}

## courses
{
  course_id: String,
  title: String,
  description: String,
  category: String,
  language: String,
  instructor_id: String,
  is_published: Boolean,
  avg_rating: Number,
  created_at: Date,
  lessons: [
    {
      lesson_id: String,
      title: String,
      attachments: [
        {
          attachment_id: String,
          title: String,
          type: String,
          url: String,
          uploaded_at: Date
        }
      ]
    }
  ]
}

## enrollments
{
  enrollment_id: String,
  user_id: String,
  course_id: String,
  course_title: String,
  completed_lessons: [String],
  progress_percentage: Number,
  status: String,
  last_accessed_at: Date
}

## quizzes
{
  quiz_id: String,
  course_id: String,
  title: String,
  passing_score: Number,
  max_attempts: Number,
  questions: [
    {
      question_id: String,
      text: String,
      options: [String],
      correct: String
    }
  ]
}

## certificates
{
  certificate_id: String,
  user_id: String,
  course_id: String,
  course_title: String,
  issue_date: Date,
  verification_code: String
}

## conversations
{
  conversation_id: String,
  course_id: String,
  participants: [String],
  last_message: {
    body: String,
    sender_id: String,
    sent_at: Date
  },
  last_message_at: Date,
  unread_by: [String],
  created_at: Date
}

## messages
{
  message_id: String,
  conversation_id: String,
  sender_id: String,
  body: String,
  attachment: {
    filename: String,
    url: String,
    type: String
  },
  sent_at: Date,
  read_at: Date
}

## announcements
{
  announcement_id: String,
  course_id: String,
  instructor_id: String,
  title: String,
  body: String,
  priority: String,
  expires_at: Date,
  created_at: Date
}

## user_announcements
{
  user_id: String,
  announcement_id: String,
  read_at: Date
}