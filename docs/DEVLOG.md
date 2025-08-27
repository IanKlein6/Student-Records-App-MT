# DEVLOG.md

### STRUCTURE:

## DATE:
- [ ✅ = done; ❌ = not applicable / removed; 🔲 = to-do; 🛠️ = in progress; 🔍 = under review ] Daily coding activities, testing, discoveries
    - What you implemented, changed, or tested; 
    - Issues encountered and how you solved or worked around them; 
    - Rough ideas you're experimenting with; 
    - Excalidraw diagram updates or sketches; 
    - Refactorings or small architecture cleanups; 
    - Local testing status / next steps


## 01-08-2025
- Finalized core database schema with all necessary tables:
  - `students`, `groups`, `student_group_memberships`, `semesters`
  - `exam_attempt_evaluation` (previously called `trials`)
  - `technika`, `availability_slots`, `appointments`

- Created an Excalidraw diagram to visually represent the data model and scheduling flow.
  - Included student progression logic and appointment creation
  - Color-coded entities and labeled arrows for clarity
  - Added conditional logic (Passed/Failed) via diamonds

- Discussed naming improvements:
  - Renamed `trials` ➝ `exam_attempt_evaluation` for clarity
  - Appointments tied to `availability_slots` (not directly to `time`)

- Added logic arrows from Passed/Failed back into `students` (to support rebooking)
- Clarified that email notifications and calendar creation are tied to appointment creation

- Next:
  - Add POST logic sketch to Excalidraw
  - Create Linear Plan with tickets for planning faze. 
  - Begin implementing backend endpoints


## 3-08-2025
- Reviewed overall app complexity: concluded this is a mid-to-large solo project with realistic scope for 2–4 months of focused part-time development.
  - Not just a CRUD app — includes retry logic, scheduling, semester transitions, access control, and external integrations.

- Finalized a practical development roadmap:
  - Phase-first backend plan: models → logic → API → frontend → auth/email → security → deploy
  - Security and email integration will be deferred until later, but key hooks will be structured into the models and routes now.
  - Testing will be continuous, with final audit before deployment.

- Created two roadmap inside of roadmap.md:
  - A **Quick Overview** (high-level phase list)
  - A **Detailed Checklist** with tasks per phase and early security markers

- Confirmed Linear issue structure:
  - Planning and implementation live in one Linear project
  - Use status flow + labels (e.g. `planning`, `excalidraw`, `backend`) instead of separate projects
  - Tickets will live in `Idea Dump` and be drawn as needed

- Decided to draw **five essential Excalidraw diagrams** before backend implementation:
  - Entity Relationship Diagram (ERD)
  - Semester & Retry Logic Flow
  - Mini System Overview (Frontend ↔ API ↔ DB)
  - Student State Lifecycle
  - Request/Response Flow (e.g., assign retry)

- Created Linear-ready descriptions for all five diagrams
  - Each includes what to draw, why it matters, and what decisions it informs

- Reconfirmed that email notifications, Firebase Auth, and deployment hardening will be implemented later — not blocked by postponing them

- Create #1 "Mini Systems Overview" of the 5 core Excalidraw diagrams:
    - mini systems overview detailing the basic overview from frontend - api - backend - DB and back. noted security checks to be added later
- Started working on #2 "Entity Relationship Diagram" of the core drawings:
    - Started remapping the first version of this. 
    - Finished Student, Exam_attempt, Group adding FK/PK 
        

- Next:
  - Draw and complete the the rest of the 4 of 5 core Excalidraw diagrams
  - Start implementing backend models and migrations
  - Add API routes for Student, Group, Semester, Attempt
  - Test routes


## 8-08-2025
- added Work Student Potential option to student and exam attempt
  - should be 3 tiered to show how strongly they want them needs to then be a visual and search or filter students by potential
  - added issue to Linear "Student Profile" for frontend later and to backend student + exam attempt model 
  - have to do some averaging math if multiple attempts have different potential scales.
- created semester student flow chart explain how the student and its exams move through the app 
- drew two excali drawings 
  - 1 semester student flow: logic showing the logic of how a student progresses through the app
  - 2 semester student flow: explained. more in depth explaining of what happens in the app in regard to the student and their attempts and interaction with the examiner and scheduling. 
- started on Diagram Request/Response Flow for critical Action
  - am quite confused and for as far as validation but having a hard time with the errors and where they need to go. might have to go simple and then add more as it starts to make more sense. 

## 09-08-2025
- Added Linear issues for all main models: Student, Semester, Evaluation, Appointment, Examiner, User
  - added sub tickets covering all important points for each model including schemas, testing, migrations and documentation. 
- Worked on refining the Student model
  - Identified that FrozenSets (sets that are immutable once created) do not work for this since they are not a Tortoise ORM field. 
    - Instead had to use CharEnumField. Creates a class with constraint options which are then added to the models field.
  - Created two Enum classes: StudentStatus and WorkPotential with their respective options. 
  - added attempt field with int
  - added created_at to see when the profile was created
  - added meta indexes last_name and first_name for easy sorting
  - single index on status for see who's active

## 2025-08-23 - Backend progress on Student model & endpoints
- Fixed test setup
    - Clarified that test_students.py is testing the FastAPI routes, not the model directly.
  - Confirmed current tests cover POST /student (success, duplicate email → 409, Location header).
- Refactored schemas
    - Moved Pydantic model creators (StudentIn, StudentOut) out of main.py into a new app/schemas/student.py.
    - Reason: avoids bloating main.py, enables re-use across multiple routers/models.
- Implemented Student endpoints in main.py
  - POST /student/ — create with trimming + lowercase email, handle duplicates with IntegrityError → 409, return 201 + Location header.
  - GET /student/{id} — fetch by primary key, return 404 if not found.
  - GET /student — list/search with optional filters (first_name, last_name, email) and pagination (limit, offset).
  - PATCH /student/{id} — partial updates with custom schema (StudentPatch), normalization via Pydantic validators, duplicate email check, return updated record.
   - DELETE /student/{id} — delete by ID, return 204 if deleted, 404 otherwise.
- Added logging to routes
 - Created dedicated logger for student operations.
 - Logging at different levels:
    - debug → request filters, incoming payloads.
    - info → successful creations, updates, number of results.
    - warning → not found cases.
    - error → DB or save errors.
- Removed duplicate model definition
  - Ensured Student model only exists in app/models/student.py (was duplicated in main.py).
- PATCH design discussion
  - Narrow PATCH (names + email only) vs Broad PATCH (include status, group, semester, etc).
  - Currently using narrow PATCH for profile fields. Other fields will be updated via domain-specific endpoints (e.g., retries, reassignments).

## 25-08-2025

ORM & Migrations
  - Extended Student Tortoise model:
    - Fields: id, first_name, last_name, email (unique), semester (FK), group (FK), status (enum), attempt_num, work_student_potential (enum), notes, created_at, updated_at.
  - Indexes: (last_name, first_name) and status.
- Set up Aerich for migrations (using app.config.TORTOISE_ORM):
  - Resolved KeyError: 'default' / config path issues.
  - Handled No such option: -m (Aerich’s migrate has no -m flag).
  - Generated migration file and applied upgrade.
- Resolved DB connectivity by using existing Dockerized Postgres (student_records_postgres on 5432).
- Fixed a NOT NULL migration failure by ensuring new schema and data alignment (ultimately applied clean migration).
- Verified resulting DB schema (columns, FKs, indexes) via psql.

API & Schemas (Pydantic v2)
  - Introduced hand-written schemas (Pydantic v2 style):
    - StudentCreate (required: first_name, last_name, email, semester_id).
    - StudentPatch (all optional): includes status, notes, group_id, work_student_potential.
    - StudentRead (response): full record with id, timestamps, etc. (semester_id, work_student_potential, group_id, notes set as optional to match DB nullability; timestamps typed as datetime).
  - StudentList (lightweight list view): includes id, first_name, last_name, status.
- Used Annotated[str, StringConstraints(...)] (Pydantic v2) instead of deprecated constr.
- Reused model enums StudentStatus and WorkPotential in schemas.
- Normalized mapping from ORM → schema using:
  - StudentRead.model_validate(obj, from_attributes=True)
  - StudentList.model_validate(obj, from_attributes=True)
    (Replaced Tortoise’s deprecated from_tortoise_orm used by auto-generated models.)
- Removed redundant in-route trimming/validation; validation now lives in schemas.
- Kept email uniqueness checks at the DB layer; return 409 on conflicts.

Endpoints (current behavior)
- GET /student — paginated list w/ filters (first_name, last_name, email), returns List[StudentList].
- GET /student/{id} — returns StudentRead, 404 if not found.
- POST /student — accepts StudentCreate, returns StudentRead; 422 on validation errors, 409 on duplicate email.
- PATCH /student/{id} — accepts StudentPatch, returns StudentRead; 404 on missing, 422 on        validation errors, 409 on email conflict; rejects empty body with 400.
- DELETE /student/{id} — currently hard delete (returns 204).
(Acceptance asked for soft delete; see Decisions/TODO.)
- All endpoints manually exercised via Swagger UI (/docs).

Tooling & Environment
- VS Code “import could not be resolved” fixed by selecting the Poetry venv interpreter.
- Confirmed Pydantic 2.11.7; switched to v2 API.
- Installed Uvicorn and resolved version constraints; running on 0.34.3.
- App runs with poetry run uvicorn app.main:app --reload; verified /docs and /openapi.json.

Manual test highlights
- Verified:
    - POST /student → 201 on success; 422 on bad email or missing required fields; 409 on duplicate email.
    - GET /student/{id} → 200 with full record; 404 if not found.
    - GET /student → returns slim list (IDs present for UI actions).
    - PATCH /student/{id} → 200 with updated record; 400 for empty body; 409 on email conflict.
    - DELETE /student/{id} → 204; 404 on non-existent ID.
- Confirmed schema serialization of datetime fields; optional DB fields mapped as optional in responses.

TODO (next)
Implement soft delete logic in DELETE /student/{id}:
await Student.filter(id=student_id).update(status=StudentStatus.ARCHIVED)
Return 204; 404 if not found.
Add plural route aliases (/students, /students/{id}) pointing to existing handlers.
Add pytest coverage for:
422 cases (bad email, missing required fields).
409 duplicate email.
404 for get/patch/delete non-existent.
Soft delete behavior (status changes to archived, not removed).
(Optional) A small lookup endpoint/usage pattern in the UI for delete-by-name UX (frontend uses /students?first_name=…&last_name=…, then deletes by ID).
(Optional) Add a scripts entry in pyproject.toml for a shorter dev command (e.g., poetry run dev → runs Uvicorn).