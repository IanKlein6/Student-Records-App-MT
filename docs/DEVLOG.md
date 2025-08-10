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