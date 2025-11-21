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
<<<<<<< HEAD
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

## 27-08-25
- Summary
  - Consolidated a robust archive/restore flow for Student, tightened PATCH semantics, normalized email handling, added dedicated endpoints for archive/restore, and made deletion soft by default with a hard-delete escape hatch. Also clarified tiny request bodies and when to choose BaseModel vs other options.
- Changes by file
  - app/models/student.py
    - Added invariant-enforcing helpers:
      - async def archive(self, reason: str | None = None) -> None
      - async def restore(self, reason: str | None = None) -> None
      - Both write to ArchiveLog, set status, and set/clear archived_at (UTC), idempotently.
    - Kept/used ArchiveAction and ArchiveLog for auditability.
    - Left is_archived convenience property.
  - app/services/students.py (new)
    - Added async def hard_delete_student(student, reason=None) -> None:
      - Logs HARD_DELETE first, then await student.delete().
  - app/schemas/student.py
    - Create/Patch validators:
      - @field_validator("email", mode="before") to strip() and lower() emails.
    - Patch model alignment:
      - group_id, semester_id, notes, work_student_potential, status supported.
    - Tiny request bodies:
      - ArchiveRequest and RestoreRequest with optional reason.
  - app/main.py
    - Create: persists semester_id; normalizes email.
    - List: adds include_archived (default False) to exclude archived rows unless requested.
    - Patch:
      - Applies all declared fields (notes, group_id, semester_id, work_student_potential, etc.).
    - Status transitions:
      - If status == ARCHIVED → call student.archive(...).
      - If currently archived and status != ARCHIVED → call student.restore(...), then set new status.
    - Email uniqueness enforced on change.
  - Archive/Restore endpoints:
    - POST /student/{id}/archive (body: {"reason": "..."} | {}) → 204
    - POST /student/{id}/restore (body: {"reason": "..."} | {}) → 204
  - Delete:
    - Soft-delete by default → student.archive(reason or "DELETE soft").
    - Hard-delete via ?hard=1 → hard_delete_student(student, reason).
  - Tortoise config:
    - Enabled use_tz=True, timezone="UTC" so archived_at is tz-aware and consistent.
- Quick checks done
    - Duplicate email on create → 409.
    - PATCH with empty body → 400.
    - PATCH status=archived sets archived_at and logs.
    - POST /student/{id}/restore clears archived_at and logs.
    - GET /student excludes archived unless include_archived=true.
    - DELETE defaults to soft; ?hard=1 performs hard delete with log.

-Suggested next steps
  Add tests for archive/restore/hard-delete flows (including idempotency).
  Expose ArchiveLog via an admin-only GET /student/{id}/archive-log.
  Enforce “archived students cannot be assigned to groups or scheduled” at the service layer.
  Plan cross-model side effects for archiving (e.g., cancel Calendar events) and move logic to a domain service when needed.

## 24-09-25
- Switch to plural REST paths
  - Migrated endpoints from /student to /students for REST consistency (collections are plural). Updated tests accordingly and ensured Location header now returns /students/{id}.
- Archive/restore model behavior fixed
  - Implemented correct semantics in Student.archive() and Student.restore(): set/clear archived_at, flip status (archived/active), persist, and log ArchiveLog entries. Removed inverted/buggy checks.
- Remove general hard delete; add admin-only hard delete
  - Removed DELETE /students/{id} (to prevent accidental data loss). Added DELETE /admin/students/{id} that calls hard_delete_student(). Wires through a lightweight require_admin dependency (bypassed when TESTING=1).
- HTTPX 0.28 testing update
  - Rewrote conftest.py client fixture to use httpx.ASGITransport(app=app) instead of deprecated AsyncClient(app=...). Fixed lifespan arg mismatch by omitting it.
- Test database bootstrapping
  - conftest.py now initializes Tortoise against sqlite://:memory: and generates schemas per test, ensuring isolation and no leftover state.
- Email normalization strategy
  - Centralized email normalization via a reusable EmailNormalized type/validator in types.py. StudentCreate and StudentPatch use it to ensure lowercase/trimmed emails without re-declaring validators everywhere.
- Integrity and uniqueness checks
  - In POST /students and PATCH /students/{id}, catch IntegrityError and return 409 “Email already exists”. In PATCH, also short-circuit if empty body (400).
- Logging cleanup
  - Standardized log event names and fields (student.create, student.patch, etc.), removed duplicate decorators and stray routes; ensured warnings/errors on not found and conflicts.
- Import/circular fixes
  - Fixed circular import by avoiding importing model symbols from the same module; collected related enums/classes in one module. Added missing FastAPI imports (Depends, Request) where needed.
- Test suite pass
  - Fixed failing tests: archive status now returns archived after POST /students/{id}/archive; admin hard delete resolves to 204; general DELETE /students/{id} is gone (404/405).


## 25-09-25
Single FastAPI app in app/main.py
-- Reduces confusion, avoids “two apps” bugs, aligns with test imports (from app.main import app).
Admin scope under /admin/* with router-level auth
-- Clear separation of concerns, least privilege, and simpler security. Tests bypass via TESTING=1.
Public delete disabled for students
-- Policy choice to prevent accidental data loss; public DELETE /students/{id} returns 404. Hard deletes are admin-only.
Hard delete via service function + audit log
-- Centralizes destructive logic and guarantees ArchiveLog(HARD_DELETE) is recorded before deletion.
Students list: filters + sorting
-- Backend supports semester_id, status (active|archived|failout), q (ILIKE first/last), and sorting (created_at default desc; optional name/email/created_at asc|desc). Combines safely and runs in DB for performance.
Default ordering = “newest first”
-- Uses created_at desc when available; falls back to id desc for stability without timestamps.
Tests create FK rows they depend on
-- When tests use semester_id, they first create Semester records to avoid FK IntegrityError.
Error handling direction for POST /students
-- Pre-check email for 409 “Email already exists”; treat other DB integrity failures (e.g., invalid FK) as 422 with a clearer message. This avoids mislabeling all IntegrityError as duplicate email.
Code style for admin route naming
-- Avoid shadowing service names; route is admin_hard_delete(), service is hard_delete_student_service() for clarity.
Pending hygiene items
-- Migrate deprecated APIs (UTC, db_index, Pydantic v2) to remove warnings before release.

## 05 to 08 -11-25
- Added PEP 257 docstrings for review standardization
  - Started reviewing all Student model, service layer, schema, and router  to add docstrings for PEP 257 compliance and readability 
  - Standardized format: imperative mood for summaries, proper Args/Returns/Raises sections
  - Added "Configuration" sections to Pydantic schemas documenting model_config settings (extra="forbid")
  - Clarified process documentation in service layer functions while maintaining PEP 257 structure
  - Updated endpoint docstrings to focus on business logic rather than HTTP mechanics (status codes, schemas already visible in decorators)

- Foreign key validation strategy clarified
  - Documented reasoning for pre-validating semester_id in create_student_service: provides clear 422 errors before database operations
  - Confirmed email uniqueness is validated by database constraints (caught via IntegrityError), not pre-checked to avoid race conditions
  - Explained optional semester_id handling: validation only runs when semester_id is explicitly provided

- Service layer error handling architecture
  - Confirmed service layer raises HTTPException for business errors (422 for invalid FK, 409 for duplicates)
  - Documented IntegrityError mapping: sqlstate codes (23505=unique, 23503=FK) translate to appropriate HTTP exceptions
  - Bare `raise` at end of exception handler preserves unknown IntegrityErrors for debugging
  - Established that routers stay thin - no try/except needed as FastAPI handles HTTPException automatically

- Pydantic schema configuration standardized
  - Added model_config = ConfigDict(extra="forbid") to StudentPatch to match StudentCreate
  - Documented rationale: catches typos in update requests, prevents silent field ignoring
  - Established pattern: input schemas (Create/Patch) use extra="forbid", output schemas (Read/List) use from_attributes=True
  - Removed duplicate `group` field from StudentPatch, keeping only `group_id`

- API security fundamentals documented
  - Reviewed 12 core security concepts: authentication (JWT), authorization (RBAC), input validation, SQL injection prevention, rate limiting, HTTPS/TLS, environment variables, CORS, password hashing, logging/monitoring, error handling, dependency security
  - Current protections identified: Tortoise ORM prevents SQL injection, Pydantic validates input, extra="forbid" catches malicious fields
  - Security gaps identified: no authentication, no authorization, no rate limiting, need HTTPS in production
  - Created security checklist prioritizing authentication, HTTPS, secrets management, rate limiting, and CORS configuration

## 16.11.25
- Added doc strings to schema_students, model_students, service_student, main, api, router_admin, conftest, logger.
- renamed several files to include their folder name plus their function name e.i. services/student.py to services/service_student.py
  - Reason: naming scheme allows for better over view when having lots of tabs open being able to see which student.py actually does what.
- renamed app/main.py to api.py because there are were two mains. One in backend/main.py and one in backend/app/main.py. app/main.py is also for apis so called it api. 
- Refactored test structure in test_api.py to use async
  - Reason: All other tests are using async as well as the functions their are testing are all async, thus it makes sense to change it for consistence and since the function should be tested exactly the way the function has also be created. 
- Changed doc string scheme to include #### in front of any heading to bold them. This makes it easy to see the important parts when glancing over the docstring. 
- Fixed doc string layout problem where doc strings didn't alway appear the same when hovering over function name.
  - Fix: removed all ':' from after a heading which then allowed for consistent presentation of the doc strings.
=======
  - am quite confused and for as far as validation but having a hard time with the errors and where they need to go. might have to go simple and then add more as it starts to make more sense.
>>>>>>> feature/student_model
