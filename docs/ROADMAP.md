# Project Roadmap

## Quick Overview
- Backend models and database
- Core logic and API
- Lightweight frontend
- Scheduling system
- Email integration
- Authentication and roles
- Deployment and hosting
- Frontend polish
- Security hardening
- Testing and final polish

---

## Phase 1: Backend Models & Database
- Define models: Student, Group, Semester, Attempt, Examiner, ExaminerAvailability
- Add status and comments to Student model
- Use Pydantic validation for all input schemas
- Implement migration setup (Aerich)
- Use .env for DB credentials and secrets
- Enable created_at / updated_at timestamps

Early security:
- Avoid exposing unsafe dev/test routes
- Structure DB access with FK constraints
- Validate all external input with schemas

## Phase 2: Core API & Retry Logic
- CRUD routes for Student, Group, Attempt
- Logic to track number of attempts per type
- Auto-calculate pass/fail and archive status
- Semester transition handling
- Return consistent status from all endpoints

Security checkpoints:
- Add scaffolding for route role enforcement
- Use FastAPI dependencies to protect critical routes
- Add basic logging of actions

## Phase 3: Lightweight Frontend
- Setup basic React + Tailwind project
- Show student list and individual records
- Display attempts and status
- Add placeholder actions (Reassign, Mark as Passed)
- Test backend integration via fetch

## Phase 4: Scheduling Logic
- Build ExaminerAvailability model and API
- Logic to assign student to open slot
- Prevent double-booking
- Mark slots as booked and link student

## Phase 5: Email & Notification Integration
- Integrate SendGrid
- Send email when student is assigned to slot
- Email templates: retry notice, assignment confirmation
- Add NotificationLog model (optional)

## Phase 6: Authentication & Role Access
- Firebase Auth integration
- Check token and role on all protected endpoints
- Admin-only routes for assignments and semester config
- Faculty see only their groups/students

## Phase 7: Deployment & Hosting
- Dockerize backend and DB
- Add production .env and secrets
- Host on Fly.io, Railway, or Render
- Set up backup policy for PostgreSQL
- Serve frontend + backend

## Phase 8: Frontend Polish
- Responsive layout + component structure
- Add color logic (pass/fail indicators)
- Search, sort, and filter for student table
- Calendar-style view for schedule
- Status icons and badges

## Phase 9: Final Security Audit
- Restrict all exposed ports
- Review role-based permissions
- Add CSP header and basic rate limiting
- Sanitize all logs
- Disable debug/error tracebacks in production

## Phase 10: Testing & Final Polish
- Unit tests for key logic (retry, pass/fail)
- Integration tests for API
- Manual testing in frontend
- Final end-to-end walkthroughs
- Export test DB for reset/restore
- Prepare demo database entries

## Final Step: Presentation
- Prepare screenshots or screen recording
- Prepare architecture and feature summary
- Clean up codebase and remove dev/debug artifacts
- Document system structure and known limitations
