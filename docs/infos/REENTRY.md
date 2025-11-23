# Returning to Project After a Break

Quick checklist to get back up to speed:

1. Read last few entries in DEVLOG.md
2. Check last 3-5 git commits (`git log --oneline -5`)
3. Check Linear/GitHub issues for last active task
4. Run backend locally and verify it starts
5. Run frontend locally (when available)
6. Skim relevant Excalidraw diagrams if needed
7. Write quick entry in DEVLOG for what you're doing today

## Quick start commands
```bash
# Backend
cd backend
poetry shell
poetry run uvicorn app.api:app --reload

# Check tests still pass
poetry run pytest

# Frontend (when ready)
cd frontend
npm run dev
```
