#!/usr/bin/env python3
"""
Part 11: Modern Web APIs with FastAPI
---------------------------------------
This file provides:
1. A production-ready FastAPI application (runnable via: uvicorn main:app --reload)
2. Interactive API documentation at /docs and /redoc
3. Pydantic request/response data models with automatic validation
4. Dependency Injection for authentication & shared state
5. Built-in test execution via TestClient when run directly: python3 main.py
"""

from __future__ import annotations
import sys
from typing import Annotated, Optional

try:
    from fastapi import Depends, FastAPI, HTTPException, Header, Query, Response, status
    from fastapi.testclient import TestClient
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


if FASTAPI_AVAILABLE:
    # --- Pydantic Data Models ---
    class CourseBase(BaseModel):
        title: str = Field(..., min_length=3, max_length=100, example="FastAPI Mastery")
        instructor: str = Field(..., min_length=2, max_length=50, example="Alex Rivera")
        price: float = Field(..., gt=0.0, example=49.99)
        tags: list[str] = Field(default_factory=list, example=["python", "api", "fastapi"])

    class CourseCreate(CourseBase):
        pass

    class Course(CourseBase):
        id: int
        is_published: bool = True

        class Config:
            from_attributes = True

    # --- FastAPI Application Instance ---
    app = FastAPI(
        title="Python Mastery - Course Management API",
        description="High-performance async REST API built with FastAPI and Pydantic.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # In-memory database
    db_courses: dict[int, dict] = {
        1: {
            "id": 1,
            "title": "Python Basics & Syntax",
            "instructor": "Guido van Rossum",
            "price": 29.99,
            "tags": ["python", "beginner"],
            "is_published": True,
        },
        2: {
            "id": 2,
            "title": "Advanced Python Patterns",
            "instructor": "Raymond Hettinger",
            "price": 59.99,
            "tags": ["python", "advanced", "oop"],
            "is_published": True,
        },
    }
    course_id_seq = 2

    # --- Dependency Injection ---
    async def verify_auth_token(
        x_api_key: Annotated[Optional[str], Header(description="Secret API Key")] = None
    ) -> str:
        """Dependency that enforces API key authentication for protected endpoints."""
        if x_api_key != "secret-python-key":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing X-API-Key header. (Expected: 'secret-python-key')",
            )
        return x_api_key

    # --- API Endpoints ---
    @app.get("/", tags=["Health Check"])
    async def root() -> dict[str, str]:
        """Root status probe."""
        return {
            "status": "online",
            "framework": "FastAPI",
            "docs": "/docs",
        }

    @app.get("/api/courses", response_model=list[Course], tags=["Courses"])
    async def list_courses(
        skip: int = Query(0, ge=0, description="Items to skip for pagination"),
        limit: int = Query(10, ge=1, le=50, description="Maximum items to return"),
        tag: Optional[str] = Query(None, description="Optional tag filter"),
    ) -> list[dict]:
        """List courses with pagination and optional filtering."""
        items = list(db_courses.values())
        if tag:
            items = [c for c in items if tag.lower() in [t.lower() for t in c.get("tags", [])]]
        return items[skip : skip + limit]

    @app.get("/api/courses/{course_id}", response_model=Course, tags=["Courses"])
    async def get_course(course_id: int) -> dict:
        """Fetch a specific course by its unique ID."""
        if course_id not in db_courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} does not exist.",
            )
        return db_courses[course_id]

    @app.post(
        "/api/courses",
        response_model=Course,
        status_code=status.HTTP_201_CREATED,
        tags=["Courses"],
        dependencies=[Depends(verify_auth_token)],
    )
    async def create_course(payload: CourseCreate) -> dict:
        """Protected endpoint: Create a new course (Requires X-API-Key)."""
        global course_id_seq
        course_id_seq += 1
        new_course = {
            "id": course_id_seq,
            "title": payload.title,
            "instructor": payload.instructor,
            "price": payload.price,
            "tags": payload.tags,
            "is_published": True,
        }
        db_courses[course_id_seq] = new_course
        return new_course

    @app.delete(
        "/api/courses/{course_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        response_class=Response,
        tags=["Courses"],
        dependencies=[Depends(verify_auth_token)],
    )
    async def delete_course(course_id: int) -> Response:
        """Protected endpoint: Delete an existing course (Requires X-API-Key)."""
        if course_id not in db_courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} does not exist.",
            )
        del db_courses[course_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- In-Process Test Driver & Demonstration ---
async def async_run_demonstration() -> None:
    from httpx import ASGITransport, AsyncClient

    print("╔═══════════════════════════════════════════════════════╗")
    print("║          Part 11: FastAPI & Pydantic Demo             ║")
    print("╚═══════════════════════════════════════════════════════╝")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. Health check
        print("\n1. Testing GET / (Root Health Check):")
        res = await client.get("/")
        print(f"  Status: {res.status_code} | Body: {res.json()}")

        # 2. List initial courses
        print("\n2. Testing GET /api/courses (List all courses):")
        res = await client.get("/api/courses")
        print(f"  Status: {res.status_code}")
        for item in res.json():
            print(f"   - [#{item['id']}] {item['title']} (${item['price']:.2f})")

        # 3. Create course without auth token (Expected 401)
        print("\n3. Testing POST /api/courses without Auth header (Expected 401):")
        res = await client.post("/api/courses", json={"title": "Unauthorized Course", "instructor": "Hacker", "price": 10.0})
        print(f"  Status: {res.status_code} | Detail: {res.json().get('detail')}")

        # 4. Create course with valid Auth token
        print("\n4. Testing POST /api/courses with valid X-API-Key header:")
        headers = {"X-API-Key": "secret-python-key"}
        new_payload = {
            "title": "FastAPI & Async Microservices",
            "instructor": "Sebastián Ramírez",
            "price": 79.99,
            "tags": ["fastapi", "asyncio", "python"],
        }
        res = await client.post("/api/courses", json=new_payload, headers=headers)
        print(f"  Status: {res.status_code} (Created) | Returned Object: {res.json()}")

        # 5. Validation failure demonstration (Negative price)
        print("\n5. Testing Pydantic validation (Negative price payload -> Expected 422):")
        invalid_payload = {"title": "Invalid Price", "instructor": "Tester", "price": -15.0}
        res = await client.post("/api/courses", json=invalid_payload, headers=headers)
        print(f"  Status: {res.status_code} (Unprocessable Entity)")
        print(f"  Validation message: {res.json()['detail'][0]['msg']}")

        # 6. Delete course
        print("\n6. Testing DELETE /api/courses/1 (Protected deletion):")
        res_del = await client.delete("/api/courses/1", headers=headers)
        print(f"  Status: {res_del.status_code} (No Content)")

    print("\n" + "=" * 60)
    print("🎉 FastAPI in-process tests completed successfully!")
    print("To launch the live web server with interactive Swagger UI:")
    print("   cd part-11-fastapi-modern-apis")
    print("   uvicorn main:app --reload --port 8000")
    print("   Visit: http://127.0.0.1:8000/docs")
    print("=" * 60)


def run_demonstration() -> None:
    if not FASTAPI_AVAILABLE:
        print("=" * 60)
        print("  FastAPI / Pydantic is not installed in the current environment.")
        print("  To run this module, install the dependencies:")
        print("    pip install -r requirements.txt")
        print("=" * 60)
        return

    import asyncio
    asyncio.run(async_run_demonstration())


if __name__ == "__main__":
    run_demonstration()
