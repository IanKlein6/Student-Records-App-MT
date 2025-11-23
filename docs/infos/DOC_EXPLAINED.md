# Documentation Structure

## What goes where

**DECISIONS.md** - Why is it structured this way?
- Architectural choices
- Technology decisions
- Naming conventions
- Data model rules

**DEVLOG.md** - What did you change today?
- Daily coding activities
- Testing and discoveries
- Issues encountered and solutions
- Refactorings and cleanups

**ARCHITECTURE.md** - What does the current structure look like?
- Folder structure
- Data flow
- Component relationships

**README.md** - High-level overview
- For new devs or your future self
- Quick start guide
- Basic usage

---

## Example Entries

### DECISIONS.md
```
## 2025-08-02: Structure backend into models/, services/, api/
Rationale: Clear separation between DB schema, business logic, and route handlers.
```

### DEVLOG.md
```
## 2025-08-03
- Moved calendar logic from models to services/calendar.py
- Added error handler module
- Fixed issue with duplicate email validation
```

### ARCHITECTURE.md
```
## Backend Folder Structure
- models/: Tortoise ORM models
- services/: Business logic (retry scheduler, calendar)
- api/: FastAPI routes
- tests/: pytest unit and integration tests

## Data Flow Example
Student fails trial → retry logic triggered → slot found → appointment created → calendar synced
```
