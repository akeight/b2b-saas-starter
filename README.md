# B2B SaaS Starter
### (Organizations + Users + Roles + Tasks)

A simple full-stack B2B SaaS project for managing **organizations**, **users**, **roles/permissions**, and **tasks** (CRUD). Built with a modern TypeScript frontend and a FastAPI + Postgres backend.


---

## Tech Stack

### Frontend (in progress)
- **TypeScript**, **React**, **Vite**

### Backend
- **Python**, **FastAPI**
- **SQLAlchemy** (ORM)
- **Postgres**
- **psycopg** (DB driver)
- **uv** (Python package manager / runner)
- **uvicorn** (ASGI server)

### Auth
- **Stytch** (authentication + session management)

---

## What This App Does

### Core Entities
- **Organizations**: Create and manage orgs
- **Users**: Authenticated via Stytch; represented in DB for app-specific data
- **Roles**: Org-scoped roles with permissions
- **Tasks**: Org-scoped tasks (optionally assignable to users)

### Key Rules
- All data access is **org-scoped**
- Server enforces authorization

---