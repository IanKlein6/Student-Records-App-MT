# Backend - Student Records API

FastAPI-based backend for managing student exam records.

## Structure

backend/
├── app/
│   ├── api.py              # FastAPI app factory & configuration
│   ├── config.py           # Tortoise ORM configuration
│   ├── models/             # Database models (Tortoise ORM)
│   │   ├── model_student.py    # Student model
│   │   ├── model_group.py      # Group model
│   │   ├── model_semester.py   # Semester model
│   │   └── archive_log.py      # Audit log model
│   ├── schemas/            # Pydantic validation schemas
│   │   └── schema_student.py   # Student request/response schemas
│   ├── routers/            # API route handlers
│   │   ├── router_student.py   # Student CRUD endpoints
│   │   └── router_admin.py     # Admin-only endpoints
│   ├── services/           # Business logic layer
│   │   └── service_student.py  # Student operations
│   ├── tests/              # Pytest test suite
│   │   ├── conftest.py         # Test fixtures & setup
│   │   ├── test_api.py         # API health checks
│   │   ├── test_students.py    # Student CRUD tests
│   │   └── test_students_filter_sorting.py  # Filter/sort tests
│   └── utilities/          # Helper functions
│       ├── logger.py           # Logging configuration
│       └── utils.py            # Utility functions
├── main.py                 # Application entry point
├── pyproject.toml          # l
 dependencies
├── ruff.toml               # Ruff linter configuration
└── tortoise_config.py      # Legacy Tortoise config

Key Files

- api.py - FastAPI application factory, registers routers and database
- config.py - Tortoise ORM configuration with model registration
- models/ - Database schema definitions using Tortoise ORM
- schemas/ - Pydantic models for request validation and response serialization
- routers/ - API endpoints grouped by resource (students, admin)
- services/ - Business logic, validation, and database operations
- tests/ - Comprehensive test suite with pytest
