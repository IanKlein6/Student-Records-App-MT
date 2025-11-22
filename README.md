# Student Records Management System

> A comprehensive FastAPI-based system for managing student exam records, tracking attempts, and coordinating scheduling for protocol and oral examinations.

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)]()

## Status: In Active Development

This project is currently in **Phase 2** of development. Core backend functionality for student management is complete, with scheduling, frontend, and authentication features planned for future phases.

---

**WARNING: This application is NOT production-ready in its current state. Additional security hardening and compliance measures are required before handling real student data.**

**Important:** This application is not currently fully functional. As parts become fully functional they will be pushed to main and then this note will be edited.

---

## Project Context

This application is a **proof-of-concept solution** designed for the Messtechnik program at the University of Freiburg, aimed at replacing their current Excel-based workflow for managing student exam records and scheduling.

**Development Status:** Personal project built independently. Once a functional prototype is complete, it will be presented to program administrators for potential adoption.

**Real-World Application:** This project solves an actual operational challenge, replacing manual spreadsheet management with a robust, scalable system. Building for a concrete use case ensures the solution addresses real user needs and operational constraints.

**Problem Being Solved:** The current Excel spreadsheet workflow for tracking student attendance, exam attempts, retry logic, and examiner scheduling creates inefficiencies, data integrity issues, and coordination challenges. This system provides a centralized, automated, and user-friendly alternative.

**Note: This is an independent initiative, not commissioned by or affiliated with the University of Freiburg. Any official deployment would require university IT security review, GDPR compliance verification, and formal approval.**

---

## Key Features

### Currently Implemented
- **Full Student CRUD Operations** - Create, read, update, and manage student records
- **Smart Archive/Restore System** - Soft delete by default with comprehensive audit logging
- **Advanced Filtering & Sorting** - Search by name, email, semester, status with flexible sorting
- **Admin-Only Hard Delete** - Destructive operations restricted to administrators
- **Comprehensive Input Validation** - Pydantic v2 schemas with strict validation rules
- **Database Migrations** - Aerich-managed schema versioning
- **Extensive Test Coverage** - pytest-based test suite with 90%+ coverage
- **RESTful API Design** - OpenAPI/Swagger documentation at `/docs`
- **Audit Logging** - Complete history of archive, restore, and delete operations

### In Development
- **Group Management** - CRUD operations for student groups
- **Semester Management** - Academic period tracking and transitions
- **Exam Attempt Tracking** - Protocol and oral exam records with retry logic
- **Examiner Scheduling** - Availability slots and appointment coordination

### Planned Features (Roadmap Phases 3-10)
- **React Frontend** - Modern UI with Tailwind CSS
- **Email Notifications** - SendGrid integration for automated notifications
- **Google Calendar Integration** - Automated appointment calendar events
- **Firebase Authentication** - User authentication with role-based access control
- **Dashboard & Analytics** - Visual status indicators and reporting
- **Responsive Design** - Mobile-friendly interface for all devices

---

## Tech Stack

### Backend (Current)
- **Framework:** FastAPI 0.115.6
- **ORM:** Tortoise-ORM 0.22.0
- **Database:** PostgreSQL 16
- **Validation:** Pydantic v2.11.7
- **Testing:** pytest 8.3.4 + pytest-asyncio + httpx
- **Migrations:** Aerich
- **Containerization:** Docker + Docker Compose
- **Python:** 3.13+

### Frontend (Planned - Phase 3)
- **Framework:** React
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **State Management:** TBD (Context API or Redux)

### Infrastructure & Services (Planned - Phases 6-7)
- **Authentication:** Firebase Auth
- **Email:** SendGrid
- **Calendar:** Google Calendar API
- **Hosting:** TBD (Fly.io, Railway, or Render)
- **CI/CD:** GitHub Actions

---

## Project Structure

```
student_records_app_mt/
├── backend/
│   ├── app/
│   │   ├── models/          # Tortoise ORM models
│   │   │   ├── model_student.py
│   │   │   ├── model_group.py
│   │   │   └── model_semester.py
│   │   ├── schemas/         # Pydantic validation schemas
│   │   │   └── schema_student.py
│   │   ├── routers/         # API route handlers
│   │   │   ├── router_student.py
│   │   │   └── router_admin.py
│   │   ├── services/        # Business logic layer
│   │   │   └── service_student.py
│   │   ├── tests/           # Pytest test suite
│   │   │   ├── conftest.py
│   │   │   ├── test_api.py
│   │   │   ├── test_students.py
│   │   │   └── test_students_filter_sorting.py
│   │   ├── api.py           # FastAPI app factory
│   │   └── config.py        # Tortoise ORM configuration
│   ├── main.py              # Application entry point
│   ├── pyproject.toml       # Poetry dependencies
│   └── .env.example         # Environment variable template
├── docs/
│   ├── DEVLOG.md            # Detailed development journal
│   ├── DECISIONS.md         # Architectural decisions log
│   ├── ROADMAP.md           # Complete development roadmap
│   └── infos/               # Setup and reference guides
├── docker-compose.yml       # Docker services configuration
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.13+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 16+** - [Download](https://www.postgresql.org/download/)
- **Poetry** - Python dependency manager ([Installation Guide](https://python-poetry.org/docs/#installation))
- **Docker & Docker Compose** (optional) - For containerized database

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/IanKlein6/Student-Records-App-MT.git
   cd Student-Records-App-MT
   ```

2. **Set up the database**

   **Option A: Using Docker (Recommended)**
   ```bash
   docker-compose up -d
   ```

   **Option B: Manual PostgreSQL Installation**
   - Install PostgreSQL 16
   - Create a database:
     ```bash
     createdb student_records
     ```

3. **Install Python dependencies**
   ```bash
   cd backend
   poetry install
   poetry shell
   ```

4. **Configure environment variables**

   Create `backend/.env` file:
   ```bash
   # Database connection
   DATABASE_URL=postgres://postgres:postgres@localhost:5432/student_records

   # Admin authentication
   ADMIN_TOKEN=your-secure-admin-token-here
   ```

   **Note:** See `backend/.env.example` for all available configuration options.

5. **Run database migrations**
   ```bash
   aerich upgrade
   ```

6. **Start the development server**
   ```bash
   poetry run uvicorn app.api:app --reload
   ```

   The API will be available at: [http://localhost:8000](http://localhost:8000)

7. **Access interactive API documentation**

   - **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## API Overview

### Student Management Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/students` | List students with filtering and sorting | No |
| `GET` | `/students/{id}` | Get student by ID | No |
| `POST` | `/students` | Create new student | No |
| `PATCH` | `/students/{id}` | Update student details | No |
| `POST` | `/students/{id}/archive` | Archive student (soft delete) | No |
| `POST` | `/students/{id}/restore` | Restore archived student | No |

### Admin Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `DELETE` | `/admin/students/{id}` | Hard delete student (permanent) | Yes (X-Admin-Token) |

### Query Parameters (GET /students)

- **Filtering:**
  - `first_name` - Filter by first name (case-insensitive)
  - `last_name` - Filter by last name (case-insensitive)
  - `email` - Filter by email (case-insensitive)
  - `semester_id` - Filter by semester ID
  - `status` - Filter by status (`active`, `archived`, `failout`)
  - `q` - Search across first and last name (case-insensitive)
  - `include_archived` - Include archived students (default: false)

- **Sorting:**
  - `sort` - Sort field and order (e.g., `name:asc`, `email:desc`, `created_at:desc`)
  - Default: newest first (`created_at:desc`)

- **Pagination:**
  - `limit` - Number of results per page (default: 100)
  - `offset` - Number of results to skip (default: 0)

**Example:**
```bash
GET /students?status=active&semester_id=1&sort=name:asc&limit=50
```

For complete API documentation with request/response examples, visit `/docs` when running the server.

---

## Testing

### Run the full test suite
```bash
poetry run pytest
```

### Run with coverage report
```bash
poetry run pytest --cov=app --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Run specific test files
```bash
poetry run pytest backend/app/tests/test_students.py -v
```

### Test Features
- In-memory SQLite for test isolation and speed
- Async test support with pytest-asyncio
- Comprehensive CRUD operation testing
- Filter and sorting validation
- Archive/restore workflow testing
- Admin authentication testing
- Error handling and edge case coverage

---

## Development Roadmap

### Completed
- [x] **Phase 1:** Backend models and database schema
  - Student, Group, Semester models
  - Tortoise ORM configuration
  - PostgreSQL setup with Docker
  - Database migrations with Aerich

- [x] **Phase 2 (In Progress):** Core Student API and business logic
  - Full CRUD operations
  - Archive/restore functionality
  - Advanced filtering and sorting
  - Audit logging
  - Comprehensive test coverage

### Upcoming
- [ ] **Phase 3:** Lightweight React frontend
- [ ] **Phase 4:** Examiner scheduling system with availability slots
- [ ] **Phase 5:** Email notifications via SendGrid
- [ ] **Phase 6:** Firebase Authentication and role-based access control
- [ ] **Phase 7:** Production deployment and hosting
- [ ] **Phase 8:** Frontend polish and UX improvements
- [ ] **Phase 9:** Security hardening and compliance audit
- [ ] **Phase 10:** Final testing, bug fixes, and documentation
- [ ] **Phase 11:** Presentation and demo preparation

**For detailed phase breakdowns and task checklists, see [ROADMAP.md](docs/ROADMAP.md).**

---

## Security & Compliance

### Current Security Implementation

**Implemented Protections:**
- **SQL Injection Prevention** - Tortoise ORM with parameterized queries
- **Input Validation** - Pydantic v2 schemas with strict type checking
- **Schema Enforcement** - `extra="forbid"` prevents malicious field injection
- **Environment-Based Secrets** - All credentials stored in `.env` files
- **Admin Authentication** - X-Admin-Token header for privileged operations
- **Soft Delete by Default** - Prevents accidental data loss
- **Comprehensive Audit Logging** - ArchiveLog tracks all sensitive operations
- **Secure Development Practices** - No secrets in code, clean git history

### Planned Security Features (Pre-Production)

**Authentication & Authorization:**
- [ ] User authentication via Firebase Auth
- [ ] Role-based access control (Admin, Faculty, Technika roles)
- [ ] Multi-factor authentication (MFA)
- [ ] Session management with secure cookies
- [ ] Automatic session timeout

**Data Protection:**
- [ ] HTTPS/TLS enforcement (production only)
- [ ] Encryption at rest for sensitive fields
- [ ] Database connection encryption
- [ ] Rate limiting to prevent abuse
- [ ] CORS configuration

**Compliance (GDPR):**
- [ ] Data export API (right to portability)
- [ ] Data deletion workflows (right to erasure)
- [ ] Data retention policies with automated cleanup
- [ ] Privacy policy and terms of service
- [ ] Consent tracking mechanisms
- [ ] Data processing agreements for third-party services

**Infrastructure:**
- [ ] Security headers (CSP, HSTS, X-Frame-Options)
- [ ] DDoS protection
- [ ] Web Application Firewall (WAF)
- [ ] Regular security updates and dependency scanning
- [ ] Automated backup and disaster recovery
- [ ] Monitoring and alerting systems

### Development Security Practices

**No Real Data in Development:**
- All testing uses mock/synthetic data only
- No real student information is used during development
- Production data access only after official university approval

**Secrets Management:**
- All sensitive credentials stored in `.env` files (gitignored)
- No hardcoded passwords, API keys, or tokens in code
- Environment variable validation on startup

**Code Quality:**
- Comprehensive PEP 257 docstrings
- Type hints throughout codebase
- Linting with Ruff
- Pre-commit hooks (planned)

---

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[DEVLOG.md](docs/DEVLOG.md)** - Detailed development journal with daily progress, decisions, and learnings
- **[DECISIONS.md](docs/DECISIONS.md)** - Architectural and design decision log with rationale
- **[ROADMAP.md](docs/ROADMAP.md)** - Complete development roadmap with phase breakdowns

These documents provide insight into the development process, architectural choices, and problem-solving approach throughout the project.

---

## Contributing

This is a personal educational project and portfolio piece. It is not currently accepting external contributions.

However, feedback and suggestions are welcome! Feel free to:
- Open an issue for bug reports or feature suggestions
- Fork the repository for your own use or learning
- Reach out with questions about the architecture or implementation

---

## Acknowledgments

- **Inspiration:** This project was inspired by the operational needs of the Messtechnik program at the University of Freiburg
- **Learning Resources:** FastAPI documentation, Tortoise ORM guides, and the broader Python community
- **Problem Domain Insight:** Feedback and requirements discussions with program staff (informal)

---

## License

This project is currently unlicensed. All rights reserved.

For inquiries about usage or collaboration, please contact the author.

---

## Contact

**Ian Klein**
GitHub: [@IanKlein6](https://github.com/IanKlein6)
Location: Freiburg, Germany

---

## About the Developer

Self-taught software developer transitioning from carpentry to software engineering. Focused on building practical, real-world solutions while mastering modern development practices, clean architecture, and professional workflows.

**Approach:** Identify real problems, build robust solutions, iterate based on feedback, and continuously improve both code and process.

---

**Built with:** FastAPI • Tortoise ORM • PostgreSQL • Python 3.13 • Poetry • Docker
