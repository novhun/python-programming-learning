# Part 13: Database Mastery with SQLAlchemy 2.0 ORM

SQLAlchemy is the gold-standard Python SQL toolkit and Object Relational Mapper (ORM). It gives application developers the full power and flexibility of SQL with the idiomatic elegance of Python object modeling.

This module focuses on **SQLAlchemy 2.0+**, which uses modern Python type annotations (`Mapped`, `mapped_column`) and standard `select()` query constructs.

---

## 📖 Key Features & Architecture

### 1. Modern Declarative Models (SQLAlchemy 2.0)
Define models subclassing `DeclarativeBase` with type-annotated columns:
```python
from datetime import datetime
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # 1-to-Many Relationship
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    # Many-to-1 Relationship
    author: Mapped[Author] = relationship(back_populates="books")
```

### 2. Engines & Connection Pooling
- `create_engine(url, echo=False, pool_size=5)` manages database socket connections.
- Connection strings:
  - SQLite: `sqlite:///app.db` or in-memory `sqlite:///:memory:`
  - PostgreSQL: `postgresql+psycopg2://user:password@localhost/dbname`
  - MySQL: `mysql+pymysql://user:password@localhost/dbname`

### 3. Modern Querying (`select()`)
SQLAlchemy 2.0 deprecated the legacy `session.query(Model)` syntax in favor of the unified `select(Model)` construct:
```python
# Filtering & Sorting
stmt = select(Book).where(Book.price > 25.0).order_by(Book.title.asc())
books = session.scalars(stmt).all()

# Joins & Aggregations
from sqlalchemy import func
stmt = (
    select(Author.name, func.count(Book.id).label("book_count"))
    .join(Author.books)
    .group_by(Author.id)
)
results = session.execute(stmt).all()
```

### 4. Eager Loading vs Lazy Loading
- **Lazy loading** (default) fires extra queries when navigating relationships (can cause $N+1$ query performance bugs).
- **Eager loading** pre-fetches relationships in a single query:
  ```python
  from sqlalchemy.orm import selectinload
  stmt = select(Author).options(selectinload(Author.books))
  authors = session.scalars(stmt).all()
  ```

---

## 🏃‍♂️ How to Run the Code

### 1. Install Dependencies
```bash
pip install -r part-13-sqlalchemy-orm/requirements.txt
```

### 2. Run the Script
```bash
python3 part-13-sqlalchemy-orm/main.py
```

---

## ✍️ Practice Exercises

1. **Tagging System (Many-to-Many)**: Create a `Tag` model and an `association_table` connecting `Book` and `Tag`. Add books with multiple tags and query all books that have the tag `"Python"`.
2. **Bulk Insertion**: Benchmark inserting 5,000 records using standard `session.add()` inside a loop versus `session.scalars(insert(Book).returning(Book), data_list)`.
3. **Optimistic Locking**: Add an `integer` column `version_id` to `Book` and use SQLAlchemy's `version_id_col` mapper argument to prevent race conditions during updates.
