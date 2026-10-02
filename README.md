# EmployeeHub - Smart Employee Management System

> Modern, professional SaaS-grade Employee Management System built for a college DevOps mini-project. Demonstrates complete CI/CD, containerization, automated testing, and cloud deployment.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black.svg)
![MySQL](https://img.shields.io/badge/Database-MySQL%208.0-orange.svg)
![Bootstrap 5](https://img.shields.io/badge/UI-Bootstrap%205-purple.svg)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)
![Deployment](https://img.shields.io/badge/Deploy-Render-success.svg)
![Tests](https://img.shields.io/badge/Testing-Pytest-green.svg)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack & Architecture](#tech-stack--architecture)
3. [Project Directory Structure](#project-directory-structure)
4. [Prerequisites](#prerequisites)
5. [Local Development Setup](#local-development-setup)
6. [Database Setup (MySQL)](#database-setup-mysql)
7. [Environment Variables](#environment-variables)
8. [Running the Application](#running-the-application)
9. [Running Automated Tests](#running-automated-tests)
10. [REST API Documentation](#rest-api-documentation)
11. [DevOps Workflow & CI/CD Pipeline](#devops-workflow--cicd-pipeline)
12. [Docker Deployment (Optional)](#docker-deployment-optional)
13. [Render Cloud Deployment Guide](#render-cloud-deployment-guide)
14. [Troubleshooting & Viva FAQs](#troubleshooting--viva-faqs)

---

## 1. Project Overview

**EmployeeHub** is a clean, modern Human Resources and Employee Management SaaS platform. It solves organizational challenges by providing:
* **Session-Based Authentication & RBAC**: Secure password hashing with Werkzeug and Admin/HR role-based authorization.
* **Employee Lifecycle Management**: Full CRUD operations for staff records (personal data, compensation, contracts, job designations, and status).
* **Organizational Structure**: Department hierarchy with constraint-checked safe deletions (preventing accidental deletion of departments with active staff).
* **Real-time Analytics Dashboard**: Dynamic KPI counters, payroll projections, and interactive Chart.js visualizations powered by real database queries.
* **DevOps Best Practices**: GitHub Actions CI automation, 12-Factor App config, automated testing, and turnkey cloud deployment configuration.

---

## 2. Tech Stack & Architecture

* **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4, Plus Jakarta Sans typography.
* **Backend**: Python Flask 3.0, Flask-SQLAlchemy 3.1 ORM, PyMySQL driver.
* **Database**: MySQL 8.0 (Production & Local) / SQLite (Automated testing & zero-config fallback).
* **Security**: Werkzeug SHA-256 password hashing, CSRF session protection, SQL injection prevention via ORM parameterization.
* **Testing**: Pytest unit & integration test suite.
* **DevOps**: Git, GitHub Actions (continuous integration), Docker (containerization), Render (PaaS cloud hosting).

---

## 3. Project Directory Structure

```text
employee-management/
│
├── app/
│   ├── models/                   # SQLAlchemy database entities
│   │   ├── __init__.py
│   │   ├── user.py               # User authentication & roles
│   │   ├── department.py         # Department model & relations
│   │   └── employee.py           # Employee records & metrics
│   ├── routes/                   # Flask route controllers & blueprints
│   │   ├── __init__.py
│   │   ├── auth.py               # Sign in, sign out, login decorators
│   │   ├── dashboard.py          # Admin dashboard & analytics
│   │   ├── employees.py          # Employee CRUD web routes
│   │   ├── departments.py        # Department CRUD web routes
│   │   └── api.py                # REST JSON API endpoints
│   ├── services/                 # Business logic & query abstraction
│   │   ├── __init__.py
│   │   ├── auth_service.py       # Authentication logic
│   │   ├── department_service.py # Department logic & safety checks
│   │   └── employee_service.py   # Employee queries, filters & stats
│   ├── static/                   # Static styling & client scripts
│   │   ├── css/
│   │   │   └── style.css         # Modern SaaS stylesheet & CSS tokens
│   │   └── js/
│   │       └── main.js           # Client interactions & modal handlers
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html             # Master layout with responsive sidebar
│   │   ├── auth/
│   │   │   └── login.html        # Modern branded sign-in screen
│   │   ├── dashboard/
│   │   │   └── index.html        # Analytics dashboard with Chart.js
│   │   ├── employees/
│   │   │   ├── index.html        # Directory with search & filters
│   │   │   ├── form.html         # Add / Edit employee form
│   │   │   └── detail.html       # Single employee profile card
│   │   ├── departments/
│   │   │   └── index.html        # Department cards & manage modals
│   │   └── errors/               # 403, 404, 500 error pages
│   └── __init__.py               # Flask application factory
│
├── tests/                        # Automated Pytest suite
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures & isolated in-memory DB
│   ├── test_auth.py              # Login, logout & access control tests
│   ├── test_employees.py         # Employee CRUD tests
│   ├── test_departments.py       # Department & safe delete tests
│   └── test_api.py               # REST API endpoints test suite
│
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions automated CI pipeline
│
├── config.py                     # Environment configuration loader
├── run.py                        # Application entry point & CLI commands
├── seed.py                       # Database seeding script (Admin, HR, data)
├── requirements.txt              # Pinned Python package dependencies
├── .env.example                  # Template for environment variables
├── .gitignore                    # Git ignore file for secrets & caches
├── Dockerfile                    # Multi-stage production container image
├── .dockerignore                 # Docker build exclusions
├── docker-compose.yml            # Local orchestration (Flask + MySQL)
├── render.yaml                   # Infrastructure-as-code spec for Render
└── README.md                     # Comprehensive project documentation
```

---

## 4. Prerequisites

Before running the application locally, ensure you have:
* **Python**: 3.10, 3.11, 3.12, or 3.13 installed
* **Git**: For version control
* **MySQL Server** (Optional for local testing, as SQLite fallback is built-in): MySQL 8.0+ or XAMPP / WampServer.

---

## 5. Local Development Setup

### Step 1: Clone or navigate to the repository
```bash
cd employee-management
```

### Step 2: Create and activate a Python virtual environment
On Windows (PowerShell):
```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

On Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 6. Database Setup (MySQL)

### Option A: Using Local MySQL Server / XAMPP

1. Log in to MySQL CLI or phpMyAdmin:
```sql
CREATE DATABASE employeehub_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Create a `.env` file in the root folder (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Update the `DATABASE_URL` in `.env`:
```ini
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employeehub_db
```

### Option B: Quick Local Testing with SQLite (Zero Config)
If you don't have MySQL installed on your computer yet, you can run locally with SQLite by setting:
```ini
USE_SQLITE=true
```
in your `.env` file. The app will seamlessly create a local `employeehub.db` file!

### Step 4: Seed Initial Data
Run the seeder script to populate default users, departments, and sample employees:
```bash
python seed.py
```

#### Default Credentials:
* **Administrator**:
  * Email: `admin@employeehub.com`
  * Password: `admin123`
  * Role: `Admin` (Full access: add/edit/delete employees & departments)
* **HR Manager**:
  * Email: `hr@employeehub.com`
  * Password: `hr123`
  * Role: `HR` (Can add/edit employees and view statistics)

---

## 7. Environment Variables

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `FLASK_APP` | Application entry point | `run.py` |
| `FLASK_ENV` | Application environment | `development` or `production` |
| `SECRET_KEY` | Flask session cryptographic key | Random string (e.g. `your-super-secret-key`) |
| `DATABASE_URL` | MySQL connection string | `mysql+pymysql://root:password@localhost:3306/employeehub_db` |
| `USE_SQLITE` | Flag to use local SQLite | `false` (set `true` for instant local testing) |
| `PORT` | Local server port | `5000` |

---

## 8. Running the Application

Start the local Flask development server:
```bash
python run.py
```
Open your browser and navigate to:
**`http://localhost:5000`**

You will be presented with the modern **EmployeeHub** sign-in portal. Click the **"Fill Admin"** or **"Fill HR"** helper buttons to autofill demo credentials!

---

## 9. Running Automated Tests

The project includes unit and integration tests powered by **Pytest**:
```bash
pytest -v
```

Tests run against an in-memory isolated database, ensuring:
1. Tests execute in under 2 seconds.
2. No local database setup or teardown is required to pass tests.
3. Tests run reliably in CI pipelines (GitHub Actions).

---

## 10. REST API Documentation

All API responses return standard JSON.

### Authentication
* `POST /api/login`: Authenticate and start session
  * Body: `{"identifier": "admin@employeehub.com", "password": "admin123"}`
* `POST /api/logout`: Terminate session

### Dashboard
* `GET /api/dashboard/stats`: Returns KPI totals, payroll sum, and department breakdown

### Employees
* `GET /api/employees`: List employees (supports query parameters: `?search=devops&status=Active&department_id=1`)
* `GET /api/employees/<id>`: Retrieve single employee details
* `POST /api/employees`: Create new employee record
* `PUT /api/employees/<id>`: Update existing employee record
* `DELETE /api/employees/<id>`: Delete employee

### Departments
* `GET /api/departments`: List all departments with headcount
* `POST /api/departments`: Create department
* `PUT /api/departments/<id>`: Update department
* `DELETE /api/departments/<id>`: Safe delete department (fails with 400 if staff are assigned)

---

## 11. DevOps Workflow & CI/CD Pipeline

This project illustrates a complete **DevOps Continuous Integration / Continuous Deployment (CI/CD)** lifecycle:

```
Developer Push / PR
       │
       ▼
GitHub Repository
       │
       ▼ (Webhook Trigger)
GitHub Actions CI Runner (.github/workflows/ci.yml)
       │
       ├── 1. Check out code
       ├── 2. Set up Python 3.11 environment
       ├── 3. Install requirements.txt + flake8
       ├── 4. Lint syntax & code standards
       └── 5. Run Pytest automated test suite
       │
       ▼ (On Green Build)
Automated CD Trigger to Render Cloud / Container Registry
```

### Pushing to GitHub:
```bash
git init
git add .
git commit -m "feat: initial commit of EmployeeHub with full CI/CD"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/employee-management.git
git push -u origin main
```
As soon as you push to `main`, GitHub Actions will automatically trigger and run the build and test pipeline under the **Actions** tab!

---

## 12. Docker Deployment (Optional)

A multi-stage, production-ready `Dockerfile` and `docker-compose.yml` are included.

### Build and Run with Docker Compose:
```bash
docker-compose up --build -d
```
This spins up both the **MySQL 8.0 container** and the **Flask Gunicorn container** connected via an internal Docker bridge network.

### Build Docker Image Manually:
```bash
docker build -t employeehub:latest .
docker run -p 5000:5000 -e SECRET_KEY="mysecret" -e USE_SQLITE="true" employeehub:latest
```

---

## 13. Render Cloud Deployment Guide

Render provides free, zero-maintenance cloud hosting for Python applications. EmployeeHub is pre-configured for turnkey Render deployment.

### Option A: Turnkey Blueprint Deployment (Recommended)
This method provisions both the **Web Service** and a **Render PostgreSQL Database** automatically using [render.yaml](file:///c:/Users/dumdi/Downloads/employee-management/render.yaml).

1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: configure render deployment with postgres support"
   git push origin main
   ```
2. Open the [Render Dashboard](https://dashboard.render.com).
3. Click **New +** > **Blueprint**.
4. Connect your GitHub repository (`DEVOPS`).
5. Render detects `render.yaml` and displays the deployment plan:
   * **Web Service**: `employeehub` (Python 3.11, Gunicorn)
   * **PostgreSQL Database**: `employeehub-db`
6. Click **Apply**.
7. Render automatically:
   * Builds the Python virtual environment and installs dependencies (including `psycopg2-binary`).
   * Connects the Web Service to the PostgreSQL database via `DATABASE_URL`.
   * Runs `python seed.py` to create tables, admin accounts, departments, and sample employees.
   * Boots the production Gunicorn server.
8. Your app will be live at `https://employeehub-xxxx.onrender.com`!

---

### Option B: Free SQLite Web Service (Zero Database Setup)
If you want a 100% free web service without creating a database service:

1. In Render Dashboard, click **New +** > **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   * **Name**: `employeehub`
   * **Language**: `Python 3`
   * **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   * **Start Command**: `python seed.py && gunicorn run:app`
4. Add **Environment Variables**:
   * `FLASK_ENV`: `production`
   * `PYTHON_VERSION`: `3.11.9`
   * `USE_SQLITE`: `true`
   * `SECRET_KEY`: (Click "Generate" or enter a secret string)
5. Click **Deploy Web Service**. The app creates a local SQLite database and seeds default accounts instantly.

---

### Default Credentials After Deployment

| Role | Email | Password |
|---|---|---|
| **System Administrator** | `admin@employeehub.com` | `admin123` |
| **HR Manager** | `hr@employeehub.com` | `hr123` |

> *Tip: You can customize default credentials by setting `DEFAULT_ADMIN_EMAIL`, `DEFAULT_ADMIN_PASSWORD`, `DEFAULT_HR_EMAIL`, and `DEFAULT_HR_PASSWORD` in your Render Environment Variables!*

---

## 14. Troubleshooting & Viva FAQs

### Q1: Why use PyMySQL instead of mysqlclient?
> `mysqlclient` requires OS-level C compilers (Visual Studio C++ build tools on Windows or gcc/libmysqlclient-dev on Linux). `PyMySQL` is pure Python, installs cleanly on any operating system, and works natively with SQLAlchemy using `mysql+pymysql://`.

### Q2: How does the application prevent SQL Injection?
> All queries use SQLAlchemy ORM parameterization. Input strings are never concatenated directly into raw SQL statements.

### Q3: How is password security handled?
> Passwords are never stored in plaintext. They are salted and hashed using Werkzeug's PBKDF2/SHA-256 implementation (`generate_password_hash` and `check_password_hash`).

### Q4: What is safe department deletion?
> The system checks relational foreign key dependencies. If `Employee.query.filter_by(department_id=dept.id).count() > 0`, the deletion is blocked with a friendly warning to protect database referential integrity.

---

### Author & License
Developed for DevOps Mini-Project. Open source under the MIT License.
