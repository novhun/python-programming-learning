# Part 15: Enterprise Database CRUD & Repository Patterns

Creating, Reading, Updating, and Deleting (CRUD) data sounds straightforward, but doing it cleanly in enterprise architectures requires disciplined design. Directly coupling database queries to HTTP handlers or CLI commands causes tight coupling, code duplication, and hard-to-test code.

This module teaches production-grade database architecture using the **Repository Pattern**, **Unit of Work (UoW)**, **Soft Deletion**, and **Atomic Transactions**.

---

## 📖 Key Architectural Patterns

### 1. The Repository Pattern
The Repository Pattern mediates between the domain/business logic and the data mapping layer (SQLAlchemy). It provides a collection-like interface for accessing domain objects:
```python
class BaseRepository[T]:
    def get_by_id(self, entity_id: int) -> T | None: ...
    def list(self, skip: int = 0, limit: int = 100) -> list[T]: ...
    def create(self, entity: T) -> T: ...
    def update(self, entity_id: int, **attributes) -> T | None: ...
    def delete(self, entity_id: int) -> bool: ...
```

### 2. The Unit of Work (UoW) Pattern
The Unit of Work maintains a list of business objects affected by a transaction and coordinates the writing out of changes and resolution of concurrency problems:
```python
with UnitOfWork(session_factory) as uow:
    user = uow.users.get_by_id(42)
    user.credits -= 50
    uow.orders.create(Order(user_id=42, amount=50))
    uow.commit()  # All or nothing atomic transaction
```

### 3. Soft Deletion vs Hard Deletion
- **Hard Deletion**: Permanently executes `DELETE FROM table WHERE id = X`. Cannot be recovered; destroys historical auditing.
- **Soft Deletion**: Adds `is_deleted: bool = False` and `deleted_at: datetime | None`.
  - When deleted: updates `is_deleted = True`.
  - All standard queries automatically filter `where(Model.is_deleted.is_(False))`.

### 4. Bulk Operations & Performance
Inserting or updating thousands of rows one-by-one is thousands of times slower than using batching:
- `session.scalars(insert(Model).returning(Model), data_list)`
- `update(Model).where(Model.id.in_(ids)).values(...)`

---

## 🏃‍♂️ How to Run the Code

### 1. Install Dependencies
```bash
pip install -r part-15-database-crud-patterns/requirements.txt
```

### 2. Run the CRUD Demonstration
```bash
python3 part-15-database-crud-patterns/main.py
```

---

## ✍️ Practice Exercises

1. **Audit Log Hook**: Extend the `BaseRepository` with an audit logger that tracks who modified which record and when.
2. **Pagination Helper**: Create a generic `PaginatedResponse[T]` DTO returning `items`, `total_count`, `page`, `page_size`, and `has_next`.
3. **Optimistic Locking**: Implement version checks in `update()` such that updating a stale record raises a `ConcurrencyException`.
