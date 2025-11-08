# 📁 `/dev` — Development Notes & Planning

This folder contains supporting files used during the development process. It includes logs, diagrams, and architectural decisions.

---

## Contents

- **`DEVLOG.md`**  
  Ongoing development journal.  
  Includes daily progress updates, implementation notes, and todos.

- **`DECISIONS.md`**  
  Record of major design choices.  
  Covers tech stack decisions, naming conventions, schema revisions, and app behavior rules.

- **`ROADMAP.md`**  
    Overall plan of the project.
    Big picture

- **`TODO.md`**  
  On going todos like a ticket system. 
  Used inconjunction with Linear.com 
---

> 🛠️ These files are **not part of the deployed app**. They exist to support structured, well-documented development.



Status code cheat sheet (your app)
  422 – Pydantic validation failed (auto by FastAPI).
  400 – Syntactically valid but semantically wrong input (rare if you use 422 well).
  401/403 – Auth/permissions.
  404 – Student/Group/Semester not found.
  409 – Unique constraint conflict (e.g., email).
  500 – Unexpected server error (log it once, return generic message).
Logging
  Log once per request (e.g., in middleware or global handlers).
  Include route, user (if known), request ID, and exception type.
  Never log secrets or full payloads blindly.
Bottom line:
  Frontend: user-friendly checks & messages.
  Pydantic: structure/validate data.
  Service: business rules, transactions, domain exceptions.
  Router/global handlers: translate to clean HTTP responses.
  DB: final guardrails.