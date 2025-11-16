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
## 24-09-25
- Use plural resource paths (/students)
    - Why: Conventional REST design uses plural for collections; improves clarity when mixing list vs. detail routes and aligns with common tooling/docs.
- Keep soft delete as “archive” + separate “restore”
    - Why: Business intent is to hide but retain records. Explicit archive/restore methods avoid ambiguity and enforce auditing through ArchiveLog.
- Remove general DELETE; add admin-only hard delete at /admin/students/{id}
    - Why: Prevent accidental destruction; reserve destructive ops for admins. Keeps the public surface safe while still supporting compliance/admin workflows.
- Centralize email normalization in types.py
    - Why: DRY. One reusable constrained/validated type prevents duplicating validators across schemas and ensures consistent lowercase/trim behavior everywhere.
- Normalize + enforce email uniqueness at API boundaries
    - Why: Catch duplicates predictably (409) and keep DB/email casing consistent, avoiding ghost duplicates due to case differences.
- Update tests to httpx 0.28 ASGITransport
    - Why: AsyncClient(app=...) was removed; ASGITransport is the supported approach. Keeps tests future-proof and stable.
- Use in-memory SQLite for tests with per-test schema generation
    - Why: Fast, isolated, no cross-test leakage. Simplifies CI and local runs.
- Standardize logging keys and messages
    - Why: Easier to grep and ship to observability stacks; consistent event names across routes simplify alerting/dashboards.
- Drop duplicate/typo’d routes and fix missing imports
    - Why: Avoid confusion in the router table and runtime errors (e.g., missing Request, Depends). Keeps the app startup clean and deterministic.

## 25-09-25
Router split & single app
-- Consolidated to a single FastAPI instance in app/main.py; backend/main.py is now only a runner. Mounted app/routers/students.py (public) and app/routers/admin.py (privileged) to keep main.py slim and maintainable.
Admin hard delete
-- Implemented DELETE /admin/students/{id} guarded by router-level require_admin (bypassed when TESTING=1). Route calls hard_delete_student_service(student, reason="ADMIN hard delete") which writes an ArchiveLog(HARD_DELETE) and deletes the row.
Public delete disabled (stub)
-- Public DELETE /students/{id} removed. Added a stub that returns 404 for any id to prevent accidental deletions and satisfy tests expecting 404 on unknown ids.
GET /students: filters + sorting
-- Added combinable filters:
semester_id (exact)
status in {active, archived, failout} (failout → FAILED)
q (ILIKE on first_name OR last_name)
-- Sorting:
Default: created_at desc (fallback id desc if no timestamp field)
Optional: name:asc|desc (last_name, first_name), first_name:*, last_name:*, email:*, created_at:*
-- Supports limit/offset for paging.
Tests
-- Added test_students_filter_sorting.py covering combined filters, sorting by name/email, and default newest-first order.
-- Fixed test isolation by generating unique emails via short UUID.
-- Created Semester rows in tests before using semester_id to avoid FK failures.
-- Root endpoint adjusted to return {"message": "Hello World"}.
-- Added/imported Path in admin router; avoided naming collisions by using hard_delete_student_service.
Bug fixes & pitfalls found
-- Avoided “two apps” issue (previously backend/main.py created a second app).
-- Avoided double prefix (/admin/admin/...) by mounting prefix in exactly one place.
-- Ensured DELETE /students/{id} returns 404 instead of 405 to match spec/tests.
Warnings & cleanup (pending)
-- Replace datetime.utcnow() → datetime.now(timezone.utc).
-- Tortoise: index=True → db_index=True.
-- Pydantic v2: move any class Config → model_config = ConfigDict(...).
-- Improve POST /students error mapping: pre-check duplicate email (409) and surface FK errors as 422 (clearer than a generic 409).
Tooling notes
-- rg (ripgrep) is system-level (brew install ripgrep); use grep -RIn if unavailable.

Next steps
-- Add groups router (public CRUD minus delete) and admin hard delete under /admin/groups/{id}.
-- Extend q to include email (optional).
-- Add OpenAPI descriptions/examples for new params.
-- Add integration tests for paging + sort stability; write negative tests for invalid status/sort values.

## 05 to 08 -11-25
- Adopt PEP 257 docstrings with team-friendly extensions
  - Why: PEP 257 provides standard docstring structure, but team preference for detailed explanations led to keeping "Process" sections in service layer functions and "Configuration" sections in schemas. Balances standards compliance with team clarity needs.

- Document errors in endpoint docstrings even though they originate in service layer
  - Why: Endpoints are the public API interface that consumers interact with. Documenting errors (422, 409, etc.) in the endpoint helps API users understand error responses without digging into service code. Acts as documentation for the entire operation.

- Pre-validate foreign keys before database operations
  - Why: Provides clear, semantic HTTP errors (422 "Invalid semester_id") rather than cryptic database errors (23503). Fails fast with meaningful messages. semester_id validation only runs when provided (respects optional nature).

- Validate email uniqueness via database constraints, not pre-checks
  - Why: Prevents race conditions. Pre-checking email existence then creating student creates window where another request could create same email between check and insert. Database UNIQUE constraint is atomic and authoritative.

- Keep routers thin - no try/except for HTTPException
  - Why: FastAPI automatically catches and formats HTTPException responses. Adding try/except in routers creates boilerplate and violates single responsibility. Service layer handles business logic and raises exceptions; routers just pass through.

- Service layer raises HTTPException for business errors
  - Why: Allows precise control over HTTP status codes and error messages. IntegrityError mapping (sqlstate 23505→409, 23503→422) translates database constraints into semantic REST errors. Unknown errors re-raised for debugging.

- Add model_config to all input schemas (Create/Patch)
  - Why: extra="forbid" catches typos and malicious fields in API requests, providing immediate feedback. Prevents silent field ignoring that leads to user confusion. Output schemas (Read/List) use from_attributes=True for ORM conversion instead.

- Never log sensitive data; use structured log messages
  - Why: Security requirement - passwords, tokens, API keys must never appear in logs. Structured messages with consistent event names (student.create, student.patch) enable grep/alerting. Include context (user ID, IP) but not secrets.

- Security implementation prioritization
  - Why: Current API has no authentication/authorization - anyone can create/delete students. Priority order: 1) JWT authentication, 2) HTTPS in production, 3) environment variables for secrets, 4) rate limiting, 5) CORS configuration. Protects against most common attacks while maintaining development velocity.

- Comprehensive error documentation in code
  - Why: Future maintainers need to understand error flow. Documented which layer handles which errors (Pydantic→422 schema, Service→business rules, Database→integrity). Comments explain sqlstate codes, bare raise rationale, race condition scenarios.

## 16.11.25
- Rename files to include folder names schema/student.py tp schema/schema_student.py
    - Why: Simplifies understanding which student.py does what when having multiple pages open. 
- All tests must be async if the function is async. 
    - Why: If the function is async then we want to test it in the way it was meant to be which is async.
    - Also all other tests are async so keeping with the scheme of the other tests. 