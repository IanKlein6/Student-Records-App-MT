# Decisions Log

## Structure

Each entry should follow this format:
```
## DD/MM/YYYY - Brief summary of decisions made
- Decision title or category
  - Why: Clear explanation of the reasoning behind the decision

Categories include:
- Structural (architecture, folder structure)
- Naming (variable names, endpoints, models)
- Architectural choices (patterns, paradigms)
- Data model rules (constraints, relationships)
- Technology choices (libraries, frameworks, tools)
- Workflow agreements (processes, conventions)
```

---

## 01/07/2025 - ORM and framework choices
- Using Tortoise ORM with FastAPI
  - Why: Simpler integration for async Python; aligns with Poetry setup

## 10/07/2025 - Database selection
- PostgreSQL chosen for long-term scaling
  - Why: More robust than SQLite and well-supported in university infra

## 15/07/2025 - Service layer architecture
- Retry scheduling logic is decoupled from student model
  - Why: Easier to test and evolve without model bloat

## 01/08/2025 - Data model and naming conventions
- Rename trials to exam_attempt_evaluation
  - Why: The term "trial" was ambiguous. The new name reflects its role as a formal record of either a protocol or oral exam attempt
- Scheduling is based on availability_slots and linked to appointments
  - Why: Instead of assigning arbitrary times, we model available time slots per Technika. Students are assigned to these slots via appointments, which allows flexible and auditable scheduling
- Appointment creation triggers both email notification and Google Calendar event creation
  - Why: To keep processes atomic and auditable, we decided the notification and calendar integration will occur at the point of appointment creation rather than manually later
- Students can re-enter exam loop based on Passed/Failed state and attempt limits
  - Why: The logic for retrying is modeled in Excalidraw as decision diamonds; if max attempts aren't reached, the student may reattempt via a new appointment

## 03/08/2025 - Planning and development strategy
- Five Core Diagrams Chosen for Initial Planning
  - Why: To keep planning lightweight but effective, five diagrams were selected as the minimum necessary to guide backend development: ERD, Retry Flow, System Overview, Student State Lifecycle, and a Request/Response Flow. Other diagrams (email, calendar UI) will be created only as needed during development
- Email and Auth Integration Deferred
  - Why: Email notifications and Firebase Auth are important but not required early. These features will be implemented after core models and APIs are complete, with structure left in place to support them
- Full Security Hardening Deferred Until Deployment
  - Why: Core security practices (e.g., input validation, .env usage) will be followed during development, but advanced hardening measures (CSP, Firebase token verification, rate limiting) will be applied closer to deployment
- Unified Linear Workflow Adopted
  - Why: Using a single Linear project with labels and status-based columns (Idea Dump → Refine → Todo → etc.) is simpler for solo development than managing multiple projects
- Backend-First Development Strategy Confirmed
  - Why: Backend model design and logic will lead the project. The frontend will be built as a lightweight shell on top, with refinement, email, and security added after the logic is working
- Diagrams Used for Orientation, Not Exhaustiveness
  - Why: Diagrams are for understanding and navigation - not full documentation. Unplanned diagrams will be created only when needed, allowing development to continue without over-planning
- Backend Role and Flow Clarified
  - Why: Confirmed that FastAPI is the core backend and not just middleware. Requests flow: Frontend → FastAPI → Tortoise ORM → PostgreSQL
- Security Layers Sketched in Architecture
  - Why: Security and validation will be handled at key points in the request lifecycle: between Frontend and FastAPI (via Firebase Auth and request validation) and between FastAPI and the database (via ORM-level schema enforcement)
- status Replaces active on Student
  - Why: A string-based status field allows for clearer state tracking ("active", "passed", "failed") than a boolean flag
- Group-Student Link Moved to Separate Table
  - Why: A separate student_group_memberships table better reflects the many-to-many relationship between students and groups and keeps students clean
- Attempts No Longer Store Group ID
  - Why: Group affiliation is not needed at the attempt level since scheduling is handled through the appointments table. This reduces redundancy
- Appointments Link Students, Technika, and Slots
  - Why: The appointments table serves as the source of truth for scheduling, tying together the student, technika, and time slot in one place

## 09/08/2025 - Model field types and indexing
- Enum fields will use CharEnumField
  - Why: Decided to use Enum because FrozenSets are not available in Tortoise
- Time Stamp created in Student
  - Why: Time stamp helps see when the student was created/when they started
- Indexes will be meta in models
  - Why: Meta instead of inline because simpler coding and overview
- Composite indexes
  - Why: Used when possible for indexes that are frequently searched

## 23/08/2025 - Student API design patterns
- Keep schemas in app/schemas/ instead of main.py for clarity and re-use
  - Why: Separation of concerns and reusability across routers
- POST /student/ must trim names and lowercase emails before saving. Duplicate emails → 409 Conflict
  - Why: Consistent data format and clear error handling
- GET endpoints split into:
  - /student/{id} → fetch one by ID, 404 if missing
  - /student → list with filters + pagination, returns always a list
  - Why: Clear separation between detail and list operations
- PATCH /student/{id} is introduced for partial updates
  - Scope limited to safe profile fields (first_name, last_name, email)
  - Business-logic fields (status, attempt_num, semester, group) will be handled by separate workflow endpoints, not raw PATCH
  - Why: Prevents accidental state corruption through general-purpose update endpoint
- DELETE /student/{id} returns 204 No Content on success, 404 if missing
  - Why: Standard REST conventions

## 25/08/2025 - Schema validation and database patterns
- Schema & Validation
  - Adopt Pydantic v2 style using Annotated + StringConstraints and built-in types like EmailStr
    - Why: Forward-compatible (v3 will deprecate con* types), better static analysis
  - Keep validation in schemas, not in route functions (aside from DB constraints like uniqueness)
    - Why: Single responsibility - schemas define and validate data shape
  - Reuse model enums (StudentStatus, WorkPotential) in schemas to guarantee consistency
    - Why: Single source of truth prevents drift between model and API
- API Shape & Data Exposure
  - Schema layering:
    - Use StudentList for list endpoints (minimal fields)
    - Use StudentRead for detail endpoints (full fields)
    - Why: Efficiency, security (don't over-expose), and clarity
  - ID-based mutations (PATCH/DELETE) remain the contract
    - Frontend performs search by name/email via list endpoint, then acts using the returned ID
    - Why: Uniqueness and safety while remaining user-friendly
- ORM ↔ Schema Mapping
  - Prefer model_validate(..., from_attributes=True) for mapping ORM objects to custom Pydantic models
    - Why: Eliminates dependency on Tortoise's auto-generated Pydantic models and their async helpers
- Migrations & Database
  - Use Aerich for Tortoise migrations, configured via app.config.TORTOISE_ORM
    - Why: Standard tool for Tortoise ORM migration management
  - Keep email unique at DB; surface 409 Conflict on violations
    - Why: Database enforces constraint atomically, prevents race conditions
  - Nullable fields in DB (e.g., semester_id, work_student_potential, group_id, notes) are represented as optional in response schemas to match reality
    - Create schema still requires semester_id
    - Why: API contract reflects actual database constraints
- Deletion Strategy
  - Switch DELETE from hard delete to soft delete by setting status="archived" and returning 204
    - Why: Matches acceptance criteria; preserves history and referential integrity
- Routing Conventions
  - Expose plural aliases to match spec (/students, /students/{id}) while keeping current paths for backward compatibility
    - Why: Aligns with REST naming without breaking existing usage

## 27/08/2025 - Archive/restore patterns and API design
- Archiving location
  - Put archive() / restore() on the Student model for now
  - Why: Centralizes invariants; ergonomic calls from anywhere; easy to evolve
  - Note: Consider moving to a service if archiving later touches cross-model side effects (e.g., cancel calendar events, detach groups)
- Hard delete policy
  - Keep hard delete in app/services/students.py (hard_delete_student)
  - Why: Likely to gain cross-model behavior; safer separation from router
- Audit logging
  - Always write ArchiveLog entries for ARCHIVE, RESTORE, and HARD_DELETE
  - Why: Traceability and compliance; supports future admin UI
- Time handling
  - Store archived_at as UTC, tz-aware (use_tz=True, timezone="UTC")
  - Why: Consistency across services and logs
- Email normalization
  - Normalize emails to lowercase + trimmed at ingress
  - Why: Prevents duplicate-appearing accounts; aligns with practical provider behavior
- API shape for archive/restore
  - Use BaseModel bodies (ArchiveRequest / RestoreRequest) with optional reason
  - Why: Clear schema, easy to extend (e.g., notify: bool, actor_id)
- Soft-delete default
  - DELETE /student/{id} performs soft delete by default; hard delete only with ?hard=1
  - Why: Safety first; preserves history unless explicitly overridden
- Listing semantics
  - GET /student excludes archived by default; opt-in via include_archived=true
  - Why: Mirrors typical "active-first" views; keeps UI uncluttered
- PATCH semantics around archiving
  - Status transitions must route through helpers:
    - Setting status=ARCHIVED → student.archive(...)
    - Changing status away from ARCHIVED → student.restore(...) first
  - Why: Guarantees status ⇄ archived_at invariants and audit logging

## 24/09/2025 - REST conventions and testing patterns
- Use plural resource paths (/students)
  - Why: Conventional REST design uses plural for collections; improves clarity when mixing list vs. detail routes and aligns with common tooling/docs
- Keep soft delete as "archive" + separate "restore"
  - Why: Business intent is to hide but retain records. Explicit archive/restore methods avoid ambiguity and enforce auditing through ArchiveLog
- Remove general DELETE; add admin-only hard delete at /admin/students/{id}
  - Why: Prevent accidental destruction; reserve destructive ops for admins. Keeps the public surface safe while still supporting compliance/admin workflows
- Centralize email normalization in types.py
  - Why: DRY. One reusable constrained/validated type prevents duplicating validators across schemas and ensures consistent lowercase/trim behavior everywhere
- Normalize + enforce email uniqueness at API boundaries
  - Why: Catch duplicates predictably (409) and keep DB/email casing consistent, avoiding ghost duplicates due to case differences
- Update tests to httpx 0.28 ASGITransport
  - Why: AsyncClient(app=...) was removed; ASGITransport is the supported approach. Keeps tests future-proof and stable
- Use in-memory SQLite for tests with per-test schema generation
  - Why: Fast, isolated, no cross-test leakage. Simplifies CI and local runs
- Standardize logging keys and messages
  - Why: Easier to grep and ship to observability stacks; consistent event names across routes simplify alerting/dashboards
- Drop duplicate/typo'd routes and fix missing imports
  - Why: Avoid confusion in the router table and runtime errors (e.g., missing Request, Depends). Keeps the app startup clean and deterministic

## 25/09/2025 - Application structure and error handling
- Router split & single app
  - Consolidated to a single FastAPI instance in app/main.py; backend/main.py is now only a runner. Mounted app/routers/students.py (public) and app/routers/admin.py (privileged) to keep main.py slim and maintainable
  - Why: Reduces confusion, avoids "two apps" bugs, aligns with test imports
- Admin hard delete
  - Implemented DELETE /admin/students/{id} guarded by router-level require_admin (bypassed when TESTING=1). Route calls hard_delete_student_service(student, reason="ADMIN hard delete") which writes an ArchiveLog(HARD_DELETE) and deletes the row
  - Why: Clear separation of destructive operations with audit trail
- Public delete disabled (stub)
  - Public DELETE /students/{id} removed. Added a stub that returns 404 for any id to prevent accidental deletions and satisfy tests expecting 404 on unknown ids
  - Why: Safety and clear API contract
- GET /students: filters + sorting
  - Added combinable filters: semester_id (exact), status in {active, archived, failout}, q (ILIKE on first_name OR last_name)
  - Sorting: Default created_at desc (fallback id desc); Optional name:asc|desc, first_name:*, last_name:*, email:*, created_at:*
  - Supports limit/offset for paging
  - Why: Flexible querying without complex query language
- Tests create FK rows they depend on
  - When tests use semester_id, they first create Semester records to avoid FK IntegrityError
  - Why: Test isolation and clarity
- Error handling direction for POST /students
  - Pre-check email for 409 "Email already exists"; treat other DB integrity failures (e.g., invalid FK) as 422 with a clearer message
  - Why: Avoids mislabeling all IntegrityError as duplicate email; provides clear feedback
- Code style for admin route naming
  - Avoid shadowing service names; route is admin_hard_delete(), service is hard_delete_student_service()
  - Why: Prevents confusion and naming collisions

## 05-08/11/2025 - Documentation and validation patterns
- Adopt PEP 257 docstrings with team-friendly extensions
  - Why: PEP 257 provides standard docstring structure, but team preference for detailed explanations led to keeping "Process" sections in service layer functions and "Configuration" sections in schemas. Balances standards compliance with team clarity needs
- Document errors in endpoint docstrings even though they originate in service layer
  - Why: Endpoints are the public API interface that consumers interact with. Documenting errors (422, 409, etc.) in the endpoint helps API users understand error responses without digging into service code. Acts as documentation for the entire operation
- Pre-validate foreign keys before database operations
  - Why: Provides clear, semantic HTTP errors (422 "Invalid semester_id") rather than cryptic database errors (23503). Fails fast with meaningful messages. semester_id validation only runs when provided (respects optional nature)
- Validate email uniqueness via database constraints, not pre-checks
  - Why: Prevents race conditions. Pre-checking email existence then creating student creates window where another request could create same email between check and insert. Database UNIQUE constraint is atomic and authoritative
- Keep routers thin - no try/except for HTTPException
  - Why: FastAPI automatically catches and formats HTTPException responses. Adding try/except in routers creates boilerplate and violates single responsibility. Service layer handles business logic and raises exceptions; routers just pass through
- Service layer raises HTTPException for business errors
  - Why: Allows precise control over HTTP status codes and error messages. IntegrityError mapping (sqlstate 23505→409, 23503→422) translates database constraints into semantic REST errors. Unknown errors re-raised for debugging
- Add model_config to all input schemas (Create/Patch)
  - Why: extra="forbid" catches typos and malicious fields in API requests, providing immediate feedback. Prevents silent field ignoring that leads to user confusion. Output schemas (Read/List) use from_attributes=True for ORM conversion instead
- Never log sensitive data; use structured log messages
  - Why: Security requirement - passwords, tokens, API keys must never appear in logs. Structured messages with consistent event names (student.create, student.patch) enable grep/alerting. Include context (user ID, IP) but not secrets
- Security implementation prioritization
  - Why: Current API has no authentication/authorization - anyone can create/delete students. Priority order: 1) JWT authentication, 2) HTTPS in production, 3) environment variables for secrets, 4) rate limiting, 5) CORS configuration. Protects against most common attacks while maintaining development velocity
- Comprehensive error documentation in code
  - Why: Future maintainers need to understand error flow. Documented which layer handles which errors (Pydantic→422 schema, Service→business rules, Database→integrity). Comments explain sqlstate codes, bare raise rationale, race condition scenarios

## 16/11/2025 - File organization and testing patterns
- Rename files to include folder names schema/student.py to schema/schema_student.py
  - Why: Simplifies understanding which student.py does what when having multiple pages open
- All tests must be async if the function is async
  - Why: If the function is async then we want to test it in the way it was meant to be which is async. Also all other tests are async so keeping with the scheme of the other tests

## 22/11/2025 - Code quality tooling and standards
- Use Ruff as the primary linter and formatter
  - Why: Ruff is significantly faster than traditional Python tools (10-100x faster than Black, Flake8, isort combined). Written in Rust, it provides all-in-one linting and formatting. Consolidates multiple tools (Black, Flake8, isort, pep8-naming) into a single configuration. Growing community adoption and active development make it a future-proof choice
- Implement pre-commit hooks for automated code quality enforcement
  - Why: Catches code quality issues before they reach the repository. Prevents commits with trailing whitespace, missing newlines, invalid YAML/JSON, or large files. Runs ruff automatically to enforce consistent code style across all commits. Reduces code review burden by catching formatting and basic errors early
- Add detect-secrets to pre-commit pipeline
  - Why: Prevents accidental commits of API keys, passwords, tokens, and other secrets. Creates a baseline file to track known false positives. Runs automatically on every commit to scan for high-entropy strings and common secret patterns. Critical for security, especially before deploying to production or sharing repository publicly
- Adopt comprehensive type hints across the codebase
  - Why: Enables static type checking with mypy to catch type errors before runtime. Improves IDE autocomplete and inline documentation. Makes code more maintainable by explicitly documenting expected parameter and return types. Facilitates refactoring by catching type mismatches across function calls. Aligns with modern Python best practices (PEP 484)
- Set line length to 100 characters (not 88 or 120)
  - Why: 100 characters balances readability with screen real estate. Wider than Black's default 88 (allows more code per line) but narrower than 120 (prevents horizontal scrolling on smaller screens). Works well with modern monitors and split-screen development
- Target Python 3.13 in ruff configuration
  - Why: Specifies the exact Python version being used in the project. Ensures ruff applies appropriate syntax rules and doesn't flag valid Python 3.13 features as errors. Aligns linter with runtime environment
- Enable specific ruff rule categories (E, F, I, N, W) rather than all rules
  - Why: Focused rule set balances code quality with pragmatism. E/W (pycodestyle) enforces PEP 8 style. F (pyflakes) catches logic errors like unused imports. I (isort) organizes imports consistently. N (pep8-naming) enforces naming conventions. Avoids overly strict rules that would require extensive codebase changes without clear benefit
- Allow unused imports in __init__.py files
  - Why: __init__.py files often import modules to expose them at the package level, even if not used within the file itself. This is a common and intentional Python pattern for creating cleaner import paths (e.g., from app.models import Student instead of from app.models.model_student import Student)
- Scope pre-commit hooks to backend directory only
  - Why: Frontend and backend have different tooling requirements. Prevents ruff from attempting to lint frontend JavaScript/TypeScript files. Keeps hook execution fast by limiting scope to relevant files. Allows frontend to use its own linting tools (ESLint, Prettier) independently

## 23/11/2025 - Documentation standards and organization
- Standardize date format to DD/MM/YYYY across all documentation files
  - Why: Consistent date format prevents confusion and makes documentation easier to scan. DD/MM/YYYY is more internationally recognized than US format (MM/DD/YYYY) and avoids ambiguity with mixed formats (DD-MM-YYYY, YYYY-MM-DD). Every date entry now includes a brief summary for quick reference
- Add Structure sections to DEVLOG.md and DECISIONS.md
  - Why: New contributors and future maintainers need clear guidelines on how to format entries. Structure section at the top provides a template and examples, ensuring consistency as the project grows. Reduces friction when making new entries
- Consolidate documentation files and remove redundancy
  - Why: Multiple overlapping files (schedual chatgpt.txt, Notes.txt) create confusion about where to look for information. Consolidating into focused, well-named files (project-planning-notes.md, Notes.txt) with clear purposes makes documentation more discoverable and maintainable
- Remove emojis from documentation files
  - Why: Emojis can cause rendering issues in different editors and terminals, don't add semantic value, and make documentation look less professional. Plain text with clear structure is more accessible and version-control friendly
- Keep documentation casual but organized
  - Why: Documentation should reflect the solo developer context and feel approachable, but still be structured enough to be useful when returning after breaks or for future collaboration. Balances personality with professionalism
- Simplify git documentation from 280 to 135 lines
  - Why: Original version had extensive duplication with commands repeated in multiple sections. Developers reference documentation for quick lookups, not comprehensive tutorials. Focused content organized by task (Daily Workflow, Common Commands, etc.) is faster to navigate
- Create separate TODO.md for current tasks vs ROADMAP.md for long-term planning
  - Why: Mixing current sprint tasks with long-term roadmap creates clutter. TODO.md tracks immediate work (Current Sprint, Backlog, Blocked), while ROADMAP.md maintains the big picture. Different cadences - TODO updates daily/weekly, ROADMAP rarely changes

## 11/01/2026 - Testing data
- Separate population data for testing
  - Decided against this and for keeping testing data inline in each test allowing more flexibility for specific testing cases and simplicity
  - Can however be changed at a future date if so needed.
