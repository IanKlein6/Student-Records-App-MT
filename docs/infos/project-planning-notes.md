# Project Planning Notes

Early planning and scoping notes from initial ChatGPT conversation.

## Time Estimate
Part-time work (evenings/weekends): 4-6 weeks for solid MVP
- Backend (models, logic, tests): 2-3 weeks
- Frontend (basic UI + integrations): 2 weeks
- Google Calendar + notifications: 1 week
- Final polish + deployment: 1 week

## Progress So Far
- Fully understood and modeled the current system
- Identified rules, edge cases, and responsibilities
- Chosen stack (PostgreSQL, Tortoise ORM, React, Google APIs)
- Defined user roles, workflows, and logic paths

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| ORM | Tortoise ORM |
| Auth | Firebase Auth |
| Email | SendGrid |
| Calendar | Google Calendar API |
| Hosting | Docker → Fly.io or university system |
| Dev Tools | pytest, Docker, dotenv, pre-commit, ruff |

## Database Schema (early version)

```
students
- id, first_name, last_name, email, active

groups
- id, name, scheduled_date, semester_id

student_group_memberships
- id, student_id, group_id

semesters
- id, name, start_date, end_date

exam_attempts (formerly "trials")
- id, student_id, group_id, type, attempt, result, comment, created_at

technika (examiners)
- id, name, email

availability_slots
- id, technika_id, start_time, end_time, status

appointments
- id, student_id, technika_id, slot_id, trial_type, calendar_event_id
```

## Development Phases

1. Backend foundation (models, migrations)
2. Basic frontend + admin tools
3. Calendar integration
4. Finalize & polish

## First Steps Checklist
- [x] Create Git repo
- [x] Setup Python virtualenv
- [x] Initialize FastAPI project
- [x] Setup PostgreSQL and connect
- [x] Create first table (Student)
- [x] Write first tests
- [ ] Add logging & error handling
- [ ] Decide frontend or backend next

## Key Questions to Answer
- Strict typing support from ORM? (Yes - chose Tortoise)
- What's the benefit of testing edge cases early? (Catch issues before UI complexity)
- Which will give faster feedback - frontend or backend first? (Backend - solid foundation)
