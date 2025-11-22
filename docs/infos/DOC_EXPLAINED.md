
DECISIONS.md = Why is it structured this way?
DEVLOG.md = What did you change in the structure today?
ARCHITECTURE.md (optional) = What does the current structure look like?
README.md = High-level overview for new devs or your future self


# ARCHITECTURE.md or /docs/structure.md EXAMPLE
# Project Architecture
## Backend Folder Structure
- `models/`: Tortoise ORM models
- `services/`: Business logic (retry scheduler, calendar)
- `api/`: FastAPI routes
- `tests/`: pytest unit and integration tests
## Data Flow Example
Student fails trial → retry logic triggered → slot found → appointment created → calendar synced



# 2. In DEVLOG.md EXAMPLE
2025-08-03:
- Moved calendar logic from models to services/calendar.py
- Added error handler module

# 1. In DECISIONS.md EXAMPLE
## 2025-08-02: Structure backend into models/, services/, api/
Rationale: Clear separation between DB schema, business logic, and route handlers.
