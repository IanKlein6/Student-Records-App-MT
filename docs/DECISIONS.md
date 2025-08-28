# DECISIONS.md

### STRUCTURE:
## DATE: DECISION description (`Structural`, `naming`, `architectural choices`) (`Naming decisions` (e.g. exam_attempt_evaluation instead of trial), `Data model rules` (e.g. max 2 attempts per type per semester), `Technology choices` (e.g. "Using Tortoise ORM with PostgreSQL"), `Workflow agreements` (e.g. “Appointments created by Technika only”), `Abstractions` (e.g. Why appointments are tied to slots))
Reason: Decision explained why


## 2025-07-01 
- Using Tortoise ORM with FastAPI
    - Reason: Simpler integration for async Python; aligns with Poetry setup


## 2025-07-10
- PostgreSQL chosen for long-term scaling
    - Reason: More robust than SQLite and well-supported in university infra


## 2025-07-15
- Retry scheduling logic is decoupled from student model
    - Reason: Easier to test and evolve without model bloat


## 2025-08-01 
- Rename `trials` to `exam_attempt_evaluation`
    - Reason: The term “trial” was ambiguous. The new name reflects its role as a formal record of either a protocol or oral exam attempt.
- Scheduling is based on `availability_slots` and linked to `appointments`
    - Reason: Instead of assigning arbitrary times, we model available time slots per Technika. Students are assigned to these slots via `appointments`, which allows flexible and auditable scheduling.
- Appointment creation triggers both email notification and Google Calendar event creation
    - Reason: To keep processes atomic and auditable, we decided the notification and calendar integration will occur at the point of appointment creation rather than manually later.
- Students can re-enter exam loop based on Passed/Failed state and attempt limits
    - Reason: The logic for retrying is modeled in Excalidraw as decision diamonds; if max attempts aren’t reached, the student may reattempt via a new appointment.


## 2025-08-03 
- Five Core Diagrams Chosen for Initial Planning
    - Reason: To keep planning lightweight but effective, five diagrams were selected as the minimum necessary to guide backend development: ERD, Retry Flow, System Overview, Student State Lifecycle, and a Request/Response Flow. Other diagrams (email, calendar UI) will be created only as needed during development.
- Email and Auth Integration Deferred
    - Reason: Email notifications and Firebase Auth are important but not required early. These features will be implemented after core models and APIs are complete, with structure left in place to support them.
- Full Security Hardening Deferred Until Deployment
    - Reason: Core security practices (e.g., input validation, .env usage) will be followed during development, but advanced hardening measures (CSP, Firebase token verification, rate limiting) will be applied closer to deployment.
- Unified Linear Workflow Adopted
    - Reason: Using a single Linear project with labels and status-based columns (Idea Dump → Refine → Todo → etc.) is simpler for solo development than managing multiple projects.
- Backend-First Development Strategy Confirmed
    - Reason: Backend model design and logic will lead the project. The frontend will be built as a lightweight shell on top, with refinement, email, and security added after the logic is working.
- Diagrams Used for Orientation, Not Exhaustiveness
    - Reason: Diagrams are for understanding and navigation — not full documentation. Unplanned diagrams will be created only when needed, allowing development to continue without over-planning.
- Backend Role and Flow Clarified  
    - Reason: Confirmed that FastAPI is the core backend and not just middleware. Requests flow: Frontend → FastAPI → Tortoise ORM → PostgreSQL.
- Security Layers Sketched in Architecture  
    - Reason: Security and validation will be handled at key points in the request lifecycle: between Frontend and FastAPI (via Firebase Auth and request validation) and between FastAPI and the database (via ORM-level schema enforcement).
- `status` Replaces `active` on Student  
    - Reason: A string-based `status` field allows for clearer state tracking (`"active"`, `"passed"`, `"failed"`) than a boolean flag.
- Group–Student Link Moved to Separate Table  
    - Reason: A separate `student_group_memberships` table better reflects the many-to-many relationship between students and groups and keeps `students` clean.
- Attempts No Longer Store Group ID  
    - Reason: Group affiliation is not needed at the `attempt` level since scheduling is handled through the `appointments` table. This reduces redundancy.
- Appointments Link Students, Technika, and Slots  
    - Reason: The `appointments` table serves as the source of truth for scheduling, tying together the student, technika, and time slot in one place.

## 09-08-25 
- Enum fields will use CharEnumField
    - Reason: decided to use Enum because FrozenSets are not available in Tortoise. 
- Time Stamp created in Student
    - Reason: time stamp helps see when the student was created/ when they started
- Indexs will be meta in models
    - Reason: meta instead of inline because simpler coding and overview. 
- Composite indexes
    - Reason: used when possible for indexes that are frequently searched

## 23-08-25 Student API Design
- Keep schemas in app/schemas/ instead of main.py for clarity and re-use.
- POST /student/ must trim names and lowercase emails before saving. Duplicate emails → 409 Conflict.
- GET endpoints split into:
    - /student/{id} → fetch one by ID, 404 if missing.
    - /student → list with filters + pagination, returns always a list.
- PATCH /student/{id} is introduced for partial updates.
    - Scope limited to safe profile fields (first_name, last_name, email).
    - Business-logic fields (status, attempt_num, semester, group) will be handled by separate workflow endpoints, not raw PATCH.
- DELETE /student/{id} returns 204 No Content on success, 404 if missing.

## 25-08-25
Schema & Validation
- Adopt Pydantic v2 style using Annotated + StringConstraints and built-in types like EmailStr.
    - Rationale: forward-compatible (v3 will deprecate con* types), better static analysis.
- Keep validation in schemas, not in route functions (aside from DB constraints like uniqueness).
- Reuse model enums (StudentStatus, WorkPotential) in schemas to guarantee consistency.

API Shape & Data Exposure
- Schema layering:
    - Use StudentList for list endpoints (minimal fields).
    - Use StudentRead for detail endpoints (full fields).
    - Rationale: efficiency, security (don’t over-expose), and clarity.
- ID-based mutations (PATCH/DELETE) remain the contract.
    - Frontend performs search by name/email via list endpoint, then acts using the returned ID.
    - Rationale: uniqueness and safety while remaining user-friendly.

ORM ↔︎ Schema Mapping
- Prefer model_validate(..., from_attributes=True) for mapping ORM objects to custom Pydantic models.
    - Rationale: eliminates dependency on Tortoise’s auto-generated Pydantic models and their async helpers.

Migrations & Database
- Use Aerich for Tortoise migrations, configured via app.config.TORTOISE_ORM.
- Keep email unique at DB; surface 409 Conflict on violations.
- Nullable fields in DB (e.g., semester_id, work_student_potential, group_id, notes) are represented as optional in response schemas to match reality.
    - Create schema still requires semester_id.

Deletion Strategy
- Decision: switch DELETE from hard delete to soft delete by setting status="archived" and returning 204.
    - Rationale: matches acceptance criteria; preserves history and referential integrity.

Routing Conventions
- Current routes use /student.
    - Decision: expose plural aliases to match spec (/students, /students/{id}) while keeping current paths for backward compatibility.
    - Rationale: aligns with REST naming without breaking existing usage.

## 27-08-25 
- Archiving location
    - Decision: Put archive() / restore() on the Student model for now.
    - Rationale: Centralizes invariants; ergonomic calls from anywhere; easy to evolve.
    - Note: Consider moving to a service if archiving later touches cross-model side effects (e.g., cancel calendar events, detach groups).
- Hard delete policy
    - Decision: Keep hard delete in app/services/students.py (hard_delete_student).
    - Rationale: Likely to gain cross-model behavior; safer separation from router.
- Audit logging
    - Decision: Always write ArchiveLog entries for ARCHIVE, RESTORE, and HARD_DELETE.
    - Rationale: Traceability and compliance; supports future admin UI.
- Time handling
    - Decision: Store archived_at as UTC, tz-aware (use_tz=True, timezone="UTC").
    - Rationale: Consistency across services and logs.
- Email normalization
    - Decision: Normalize emails to lowercase + trimmed at ingress.
    - Rationale: Prevents duplicate-appearing accounts; aligns with practical provider behavior.
- API shape for archive/restore
    - Decision: Use BaseModel bodies (ArchiveRequest / RestoreRequest) with optional reason.
    - Rationale: Clear schema, easy to extend (e.g., notify: bool, actor_id).
- Soft-delete default
    - Decision: DELETE /student/{id} performs soft delete by default; hard delete only with ?hard=1.
    - Rationale: Safety first; preserves history unless explicitly overridden.
- Listing semantics
    - Decision: GET /student excludes archived by default; opt-in via include_archived=true.
    - Rationale: Mirrors typical “active-first” views; keeps UI uncluttered.
- PATCH semantics around archiving
    - Decision: Status transitions must route through helpers:
        - Setting status=ARCHIVED → student.archive(...).
        - Changing status away from ARCHIVED → student.restore(...) first.
        - Rationale: Guarantees status ⇄ archived_at invariants and audit logging.