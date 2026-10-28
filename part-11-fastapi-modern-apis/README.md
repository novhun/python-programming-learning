# Part 11: Modern Web APIs with FastAPI

FastAPI is a modern, high-performance web framework for building APIs with Python 3.10+ based on standard Python type hints. Built on top of **Starlette** (for async web routing) and **Pydantic** (for data validation and serialization), FastAPI is one of the fastest and most productive frameworks available.

---

## 📖 Key Features

### 1. Automatic Interactive Documentation
FastAPI automatically generates interactive API documentation out of the box using OpenAPI standards:
- **Swagger UI**: Navigate to `http://127.0.0.1:8000/docs`
- **ReDoc**: Navigate to `http://127.0.0.1:8000/redoc`

### 2. Request Validation with Pydantic
Declare request payloads and response shapes using standard Pydantic models:
```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0.0)
    description: str | None = None
```
FastAPI automatically validates incoming JSON against this schema, rejecting malformed inputs with detailed HTTP 422 error messages.

### 3. Route Handlers & Parameters
- **Path Parameters**: Extract variables from URL path:
  ```python
  @app.get("/items/{item_id}")
  async def get_item(item_id: int):
      ...
  ```
- **Query Parameters**: Automatically inferred from function arguments not in the path:
  ```python
  @app.get("/items")
  async def list_items(skip: int = 0, limit: int = 10):
      ...
  ```
- **Request Body**: Automatically parsed from JSON when declared with a Pydantic model:
  ```python
  @app.post("/items", status_code=201)
  async def create_item(payload: ItemCreate):
      ...
  ```

### 4. Dependency Injection (`Depends`)
FastAPI features a powerful dependency injection system used for:
- Database sessions
- Authentication and authorization (Bearer tokens, API keys)
- Shared pagination logic
```python
from fastapi import Depends, Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret-token-123":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/protected", dependencies=[Depends(verify_api_key)])
async def secret_endpoint():
    return {"status": "authorized"}
```

---

## 🏃‍♂️ How to Run the Code

### 1. Install Dependencies
```bash
pip install -r part-11-fastapi-modern-apis/requirements.txt
```

### 2. Run the In-Process Verification Script
The accompanying `main.py` can be executed directly as a standard script to test all endpoints automatically:
```bash
python3 part-11-fastapi-modern-apis/main.py
```

### 3. Start the Live Development Server (Uvicorn)
```bash
cd part-11-fastapi-modern-apis
uvicorn main:app --reload --port 8000
```
Then visit `http://127.0.0.1:8000/docs` in your browser.

---

## ✍️ Practice Exercises

1. **User Registration API**: Create a `POST /users` endpoint accepting `username`, `email`, and `password`. Use Pydantic field validators to ensure passwords are at least 8 characters long and emails contain `@`.
2. **Filtering and Pagination**: Add query parameters `min_price`, `max_price`, `category`, `page`, and `per_page` to `GET /products`, returning matching items with pagination metadata.
3. **JWT Authentication**: Research OAuth2 with Password (and hashing) using `passlib` and `python-jose` to issue and verify JWT bearer tokens.
