# Part 12: Enterprise Full-Stack Web Development with Django

Django is the industry-standard, "batteries-included" Python web framework. This module is structured according to **professional enterprise standards**, featuring clean separation between project configuration, application domain logic, data models, forms, web templates, and RESTful API endpoints.

---

## 🏗️ Professional Project Directory Structure

```
part-12-django-web-framework/
├── manage.py                          # Standard Django CLI administrative tool
├── main.py                            # Course test runner & development server entrypoint
├── requirements.txt                   # Project dependencies (django>=5.0.0)
├── README.md                          # Comprehensive documentation & architecture guide
│
├── course_project/                    # Project Configuration Package
│   ├── __init__.py
│   ├── settings.py                    # Global configuration (Apps, Middleware, DB, Templates)
│   ├── urls.py                        # Root URL routing dispatcher
│   ├── wsgi.py                        # WSGI entrypoint for production servers (Gunicorn)
│   └── asgi.py                        # ASGI entrypoint for async servers (Uvicorn/Daphne)
│
├── courses/                           # Domain Application (Courses App)
│   ├── __init__.py
│   ├── apps.py                        # AppConfig (CoursesConfig)
│   ├── models.py                      # Database models (Course)
│   ├── forms.py                       # ModelForm definitions with validation (CourseForm)
│   ├── admin.py                       # Django Admin customization & registration
│   ├── views.py                       # Full-Stack Web UI views (HTML template rendering)
│   ├── api_views.py                   # RESTful JSON API views (CRUD endpoints)
│   ├── urls.py                        # App-level URL routes (UI & API endpoints)
│   └── migrations/                    # Database schema migration versioning
│       ├── __init__.py
│       └── 0001_initial.py
│
└── templates/                         # HTML5 Presentation Layer
    ├── base.html                      # Root layout (Navbar, CSS, Flash alerts, Footer)
    └── courses/                       # Namespaced App Templates
        ├── course_list.html           # Catalog dashboard with cards, stats & search
        ├── course_form.html           # Create & Edit form with ModelForm rendering
        └── course_confirm_delete.html # Deletion confirmation safety screen
```

---

## 🌟 Architectural Features

### 1. Model-Form Integration (`CourseForm`)
Instead of parsing raw `request.POST` manually, Django's `ModelForm` automatically generates widgets, handles type conversion, sanitizes inputs, and runs field validators (e.g., preventing negative prices).

### 2. Separation of UI Views and API Views
- **`courses/views.py`**: Handles user-facing HTTP requests, template rendering, and flash notification messages (`messages.success`).
- **`courses/api_views.py`**: Handles machine-to-machine JSON requests with standard HTTP status codes (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`).

### 3. RESTful API Endpoints
| HTTP Method | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/api/courses/` | List all courses (supports `?search=...` and `?category=...`) |
| `POST` | `/api/courses/` | Create a new course from JSON payload |
| `GET` | `/api/courses/<id>/` | Retrieve details for a single course |
| `PUT` / `PATCH` | `/api/courses/<id>/` | Update course fields via JSON payload |
| `DELETE` | `/api/courses/<id>/` | Permanently delete course by ID |

---

## 🏃‍♂️ How to Run

### 1. Install Dependencies
```bash
pip install -r part-12-django-web-framework/requirements.txt
```

### 2. Run Automated Verification Suite
Verifies both Web UI routes and JSON API endpoints programmatically:
```bash
python3 part-12-django-web-framework/main.py
```

### 3. Start the Interactive Development Server
```bash
# Using main.py runner:
python3 part-12-django-web-framework/main.py runserver 8000

# Or using standard Django manage.py:
cd part-12-django-web-framework
python3 manage.py runserver 8000
```

Then open your browser:
- 🌐 **Web Catalog UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- ➕ **Add Course Form**: [http://127.0.0.1:8000/courses/create/](http://127.0.0.1:8000/courses/create/)
- ⚡ **REST API Endpoint**: [http://127.0.0.1:8000/api/courses/](http://127.0.0.1:8000/api/courses/)
- 🛠️ **Django Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
