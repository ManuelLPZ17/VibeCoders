 # Modelo de Datos — MongoDB

## users
RF05 — Registro de usuarios. El campo `role` distingue entre estudiante e instructor.
El `_id` de MongoDB funciona como identificador principal. Índices únicos sobre `email`.

```json
{
  "_id": ObjectId,
  "username": "manuel_lp",
  "email": "manuel@iteso.mx",
  "hashed_password": "$2b$12$...",
  "role": "student",
  "created_at": ISODate("2026-01-15T10:00:00Z")
}
```

---

## courses
RF01, RF02, RF04 — Cursos publicados. Las lecciones y sus materiales adjuntos se almacenan
como subdocumentos embebidos dentro del array `lessons`. Esta decisión de embedding evita
joins adicionales ya que el patrón de acceso casi siempre requiere el curso completo con
sus lecciones.

```json
{
  "_id": ObjectId,
  "title": "Introducción a Python",
  "description": "Aprende los fundamentos...",
  "category": "programming",
  "language": "es",
  "instructor_id": ObjectId,
  "is_published": true,
  "avg_rating": 4.7,
  "created_at": ISODate("2025-09-01T00:00:00Z"),
  "lessons": [
    {
      "lesson_id": "les_0047",
      "title": "Variables y tipos",
      "content": "...",
      "attachments": [
        {
          "attachment_id": "att_001",
          "title": "Guía PDF",
          "type": "pdf",
          "url": "https://storage/.../guia.pdf",
          "uploaded_at": ISODate("2025-09-05T00:00:00Z")
        }
      ]
    }
  ]
}
```

---

## enrollments
RF03, RF09 — Inscripción de un estudiante a un curso. El array `completed_lessons` contiene
los `lesson_id` finalizados. `progress_percentage` se calcula con base en este array.
`course_title` se desnormaliza para mostrar el historial sin requerir un lookup adicional.

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "course_id": ObjectId,
  "course_title": "Introducción a Python",
  "completed_lessons": ["les_0047", "les_0048"],
  "progress_percentage": 75.0,
  "status": "in_progress",
  "last_accessed_at": ISODate("2026-04-24T18:00:00Z")
}
```

---

## quizzes
RF07 — Evaluaciones del curso. Las preguntas se almacenan embebidas. `passing_score` y
`max_attempts` permiten al instructor configurar criterios de aprobación por evaluación.

```json
{
  "_id": ObjectId,
  "course_id": ObjectId,
  "title": "Examen módulo 1",
  "passing_score": 70,
  "max_attempts": 3,
  "questions": [
    {
      "question_id": "q_001",
      "text": "¿Qué es una variable?",
      "options": ["A", "B", "C", "D"],
      "correct": "A"
    }
  ]
}
```

---

## certificates
RF08 — Certificados emitidos al completar un curso. `verification_code` es único e indexado
para permitir validación externa sin autenticación.

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "course_id": ObjectId,
  "course_title": "Introducción a Python",
  "issue_date": ISODate("2026-04-20T00:00:00Z"),
  "verification_code": "VC-2026-XK9T"
}
```

---

## conversations
RF06 — Mensajes directos entre estudiante e instructor. `last_message` se desnormaliza para
renderizar el inbox sin consultar la colección `messages`. `unread_by` es un array de
ObjectId con multi-key index para detectar no leídos eficientemente.

```json
{
  "_id": ObjectId,
  "course_id": ObjectId,
  "participants": [ObjectId, ObjectId],
  "last_message": {
    "body": "Profe, tengo duda con el ejercicio 3...",
    "sender_id": ObjectId,
    "sent_at": ISODate("2026-04-24T15:00:00Z")
  },
  "unread_by": [ObjectId],
  "created_at": ISODate("2026-04-20T09:00:00Z")
}
```

---

## messages
RF06 — Mensajes individuales dentro de una conversación. Referencia a `conversations._id`
mediante `conversation_id`.

```json
{
  "_id": ObjectId,
  "conversation_id": ObjectId,
  "sender_id": ObjectId,
  "body": "Profe, tengo duda con el ejercicio 3...",
  "attachment": {
    "filename": "captura.png",
    "url": "https://storage/.../captura.png",
    "type": "image/png"
  },
  "sent_at": ISODate("2026-04-24T15:00:00Z"),
  "read_at": null
}
```

---

## announcements
RF10 — Anuncios del instructor para los estudiantes de un curso. Índice TTL sobre `expires_at`
para eliminación automática de anuncios vencidos. `total_enrolled` se guarda para calcular
la tasa de lectura sin consultas adicionales.

```json
{
  "_id": ObjectId,
  "course_id": ObjectId,
  "instructor_id": ObjectId,
  "title": "Cambio de fecha — Examen módulo 3",
  "body": "El examen se pospone al viernes 2 de mayo...",
  "priority": "high",
  "expires_at": ISODate("2026-05-03T00:00:00Z"),
  "created_at": ISODate("2026-04-24T14:00:00Z"),
  "total_enrolled": 38
}
```

---

## user_announcements
RF10 — Registro de lecturas por usuario. Se separa de `announcements` para evitar que
el documento crezca con el array de lecturas conforme aumentan los estudiantes.

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "announcement_id": ObjectId,
  "read_at": ISODate("2026-04-24T16:00:00Z")
}
```
