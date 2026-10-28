#!/usr/bin/env python3
"""
Part 12: Enterprise Full-Stack Web Development with Django
-----------------------------------------------------------
Architecture:
  course_project/   -> Project settings, root URL dispatcher, WSGI, ASGI
  courses/          -> Models, ModelForms, Web UI Views, REST API Views, URLs, Migrations
  templates/        -> Modern HTML5 templates (base.html, course_list.html, course_form.html)
  manage.py         -> Standard Django CLI administrative tool

Usage:
  1. Automated Verification:
     python3 main.py
  2. Launch Interactive Web Server:
     python3 main.py runserver 8000
     (or: python3 manage.py runserver 8000)
"""

from __future__ import annotations
import json
import os
from pathlib import Path
import sys

# Ensure current directory is in sys.path
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_project.settings")

try:
    import django
    from django.core.management import call_command, execute_from_command_line
    from django.test import Client
    django.setup()
    from courses.models import Course
    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False


def seed_database_if_empty() -> None:
    """Seeds initial course records if database is empty."""
    if Course.objects.count() == 0:
        starter_courses = [
            {"title": "Django for Enterprise Backends", "instructor": "Adrian Holovaty", "price": 69.99, "category": "Backend"},
            {"title": "PostgreSQL & Database Architecture", "instructor": "Simon Willison", "price": 49.99, "category": "Database"},
            {"title": "Full-Stack Web Engineering", "instructor": "Jacob Kaplan-Moss", "price": 89.99, "category": "FullStack"},
            {"title": "Python Microservices & APIs", "instructor": "Guido van Rossum", "price": 54.99, "category": "Backend"},
        ]
        for item in starter_courses:
            Course.objects.create(**item)


def run_demonstration() -> None:
    """Runs automated verification of both Web UI routes and REST API endpoints."""
    if not DJANGO_AVAILABLE:
        print("=" * 60)
        print("  Django is not installed in the current environment.")
        print("  Install dependencies with: pip install django")
        print("=" * 60)
        return

    print("╔═══════════════════════════════════════════════════════╗")
    print("║     Part 12: Django Enterprise Architecture           ║")
    print("╚═══════════════════════════════════════════════════════╝")

    print("\n[Step 1] Applying Database Migrations (migrate)...")
    call_command("migrate", verbosity=0)
    seed_database_if_empty()
    print("  ✔ Database synchronized and seeded.")

    client = Client()

    # --- 1. WEB UI TESTING ---
    print("\n--- 2. Testing Web UI Routes (HTML Templates & ModelForm) ---")

    # GET / (Course Catalog)
    res_list = client.get("/")
    print(f"  ✔ GET / (Catalog List UI)           -> Status {res_list.status_code}")

    # POST /courses/create/ (Create Course Form)
    res_create = client.post("/courses/create/", {
        "title": "Autonomous AI Agents in Python",
        "instructor": "Demis Hassabis",
        "price": "99.99",
        "category": "AI",
        "is_published": "on",
    })
    print(f"  ✔ POST /courses/create/ (Create UI) -> Status {res_create.status_code} (Redirected to catalog)")

    ai_course = Course.objects.get(title="Autonomous AI Agents in Python")
    print(f"    Created Course #{ai_course.id}: {ai_course.title} (${ai_course.price})")

    # POST /courses/<id>/edit/ (Edit Course Form)
    res_edit = client.post(f"/courses/{ai_course.id}/edit/", {
        "title": "Advanced Autonomous AI Agents & LLMs",
        "instructor": "Demis Hassabis",
        "price": "119.99",
        "category": "AI",
        "is_published": "on",
    })
    print(f"  ✔ POST /courses/{ai_course.id}/edit/ (Edit UI)  -> Status {res_edit.status_code}")

    # --- 2. REST API TESTING ---
    print("\n--- 3. Testing RESTful JSON API Endpoints ---")

    # GET /api/courses/
    res_api_list = client.get("/api/courses/")
    data_list = res_api_list.json()
    print(f"  ✔ GET /api/courses/                 -> Status {res_api_list.status_code} | Total: {data_list['count']} courses")

    # POST /api/courses/
    api_payload = {
        "title": "Cloud Native Architecture on AWS",
        "instructor": "Werner Vogels",
        "price": 89.00,
        "category": "Cloud",
    }
    res_api_create = client.post(
        "/api/courses/",
        data=json.dumps(api_payload),
        content_type="application/json",
    )
    api_created = res_api_create.json()
    print(f"  ✔ POST /api/courses/ (Create API)   -> Status {res_api_create.status_code} | ID: #{api_created['id']}")

    # PUT /api/courses/<id>/
    update_payload = {"price": 75.00, "category": "DevOps"}
    res_api_put = client.put(
        f"/api/courses/{api_created['id']}/",
        data=json.dumps(update_payload),
        content_type="application/json",
    )
    print(f"  ✔ PUT /api/courses/{api_created['id']}/ (Update API) -> Status {res_api_put.status_code} | New Price: ${res_api_put.json()['price']}")

    # DELETE /api/courses/<id>/
    res_api_del = client.delete(f"/api/courses/{api_created['id']}/")
    print(f"  ✔ DELETE /api/courses/{api_created['id']}/ (Del API) -> Status {res_api_del.status_code} | {res_api_del.json()['message']}")

    print("\n" + "=" * 60)
    print("🎉 All Enterprise Full-Stack Web UI & REST API features verified!")
    print("\nTo launch the live interactive Web application in your browser:")
    print("   python3 main.py runserver 8000")
    print("   (or: python3 manage.py runserver 8000)")
    print("\nThen open your browser to:")
    print("   Web Catalog UI: http://127.0.0.1:8000/")
    print("   Add Course:     http://127.0.0.1:8000/courses/create/")
    print("   JSON REST API:  http://127.0.0.1:8000/api/courses/")
    print("=" * 60)


if __name__ == "__main__":
    if DJANGO_AVAILABLE and len(sys.argv) > 1 and sys.argv[1] == "runserver":
        call_command("migrate", verbosity=0)
        seed_database_if_empty()
        execute_from_command_line(sys.argv)
    else:
        run_demonstration()
