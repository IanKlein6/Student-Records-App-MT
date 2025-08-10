# DECISIONS.md

### STRUCTURE:
## DATE: DECISION description (`Structural`, `naming`, `architectural choices`) (`Naming decisions` (e.g. exam_attempt_evaluation instead of trial), `Data model rules` (e.g. max 2 attempts per type per semester), `Technology choices` (e.g. "Using Tortoise ORM with PostgreSQL"), `Workflow agreements` (e.g. “Appointments created by Technika only”), `Abstractions` (e.g. Why appointments are tied to slots))
Reason: Decision explained why




## 2025-07-01: Using Tortoise ORM with FastAPI
Reason: Simpler integration for async Python; aligns with Poetry setup


## 2025-07-10: PostgreSQL chosen for long-term scaling
Reason: More robust than SQLite and well-supported in university infra


## 2025-07-15: Retry scheduling logic is decoupled from student model
Reason: Easier to test and evolve without model bloat


## 2025-08-01 Rename `trials` to `exam_attempt_evaluation`
Reason: The term “trial” was ambiguous. The new name reflects its role as a formal record of either a protocol or oral exam attempt.

## 2025-08-01 Scheduling is based on `availability_slots` and linked to `appointments`
Reason: Instead of assigning arbitrary times, we model available time slots per Technika. Students are assigned to these slots via `appointments`, which allows flexible and auditable scheduling.

## 2025-08-01 Appointment creation triggers both email notification and Google Calendar event creation
Reason: To keep processes atomic and auditable, we decided the notification and calendar integration will occur at the point of appointment creation rather than manually later.

## 2025-08-01 Students can re-enter exam loop based on Passed/Failed state and attempt limits
Reason: The logic for retrying is modeled in Excalidraw as decision diamonds; if max attempts aren’t reached, the student may reattempt via a new appointment.


## 2025-08-03 Five Core Diagrams Chosen for Initial Planning
Reason: To keep planning lightweight but effective, five diagrams were selected as the minimum necessary to guide backend development: ERD, Retry Flow, System Overview, Student State Lifecycle, and a Request/Response Flow. Other diagrams (email, calendar UI) will be created only as needed during development.

## 2025-08-03 Email and Auth Integration Deferred
Reason: Email notifications and Firebase Auth are important but not required early. These features will be implemented after core models and APIs are complete, with structure left in place to support them.

## 2025-08-03 Full Security Hardening Deferred Until Deployment
Reason: Core security practices (e.g., input validation, .env usage) will be followed during development, but advanced hardening measures (CSP, Firebase token verification, rate limiting) will be applied closer to deployment.

## 2025-08-03 Unified Linear Workflow Adopted
Reason: Using a single Linear project with labels and status-based columns (Idea Dump → Refine → Todo → etc.) is simpler for solo development than managing multiple projects.

## 2025-08-03 Backend-First Development Strategy Confirmed
Reason: Backend model design and logic will lead the project. The frontend will be built as a lightweight shell on top, with refinement, email, and security added after the logic is working.

## 2025-08-03 Diagrams Used for Orientation, Not Exhaustiveness
Reason: Diagrams are for understanding and navigation — not full documentation. Unplanned diagrams will be created only when needed, allowing development to continue without over-planning.

## 2025-08-03 Backend Role and Flow Clarified  
Reason: Confirmed that FastAPI is the core backend and not just middleware. Requests flow: Frontend → FastAPI → Tortoise ORM → PostgreSQL.

## 2025-08-03 Security Layers Sketched in Architecture  
Reason: Security and validation will be handled at key points in the request lifecycle: between Frontend and FastAPI (via Firebase Auth and request validation) and between FastAPI and the database (via ORM-level schema enforcement).

## 2025-08-03 `status` Replaces `active` on Student  
Reason: A string-based `status` field allows for clearer state tracking (`"active"`, `"passed"`, `"failed"`) than a boolean flag.

## 2025-08-03 Group–Student Link Moved to Separate Table  
Reason: A separate `student_group_memberships` table better reflects the many-to-many relationship between students and groups and keeps `students` clean.

## 2025-08-03 Attempts No Longer Store Group ID  
Reason: Group affiliation is not needed at the `attempt` level since scheduling is handled through the `appointments` table. This reduces redundancy.

## 2025-08-03 Appointments Link Students, Technika, and Slots  
Reason: The `appointments` table serves as the source of truth for scheduling, tying together the student, technika, and time slot in one place.