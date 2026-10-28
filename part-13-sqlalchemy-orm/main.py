#!/usr/bin/env python3
"""
Part 13: Database Mastery with SQLAlchemy 2.0 ORM
--------------------------------------------------
This runnable script demonstrates:
1. Modern DeclarativeBase schema creation
2. Session transaction management (commit & rollback)
3. One-to-Many relational insertions
4. Modern 2.0 select() queries and scalars()
5. Preventing N+1 queries with eager loading (selectinload)
6. Joins and aggregate calculations (func.count, func.avg)
7. Cascade deletion behavior
"""

from __future__ import annotations
import sys

try:
    from sqlalchemy import create_engine, func, select
    from sqlalchemy.orm import Session, selectinload
    from models import Author, Base, Book, Review
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def run_demonstration() -> None:
    if not SQLALCHEMY_AVAILABLE:
        print("=" * 60)
        print("  SQLAlchemy is not installed in the current environment.")
        print("  To run this module, install the dependency:")
        print("    pip install -r requirements.txt")
        print("  Or:")
        print("    pip install sqlalchemy")
        print("=" * 60)
        return

    print("╔═══════════════════════════════════════════════════════╗")
    print("║        Part 13: SQLAlchemy 2.0 ORM Mastery           ║")
    print("╚═══════════════════════════════════════════════════════╝")

    # 1. Initialize SQLite in-memory database engine
    engine = create_engine("sqlite:///:memory:", echo=False)
    print("Creating tables in-memory via Base.metadata.create_all(engine)...")
    Base.metadata.create_all(engine)
    print("Tables created: authors, books, reviews.")

    # 2. Insert records with relationships
    section("1. Relational Inserts with Session Context")
    with Session(engine) as session:
        # Create Authors
        guido = Author(name="Guido van Rossum", email="guido@python.org")
        martin = Author(name="Martin Fowler", email="martin@martinfowler.com")

        # Create Books linked to Guido
        book1 = Book(title="The Python Reference Manual", isbn="978-0131103627", price=39.99, author=guido)
        book2 = Book(title="Advanced Python Internals", isbn="978-0201633610", price=54.99, author=guido)

        # Create Reviews
        rev1 = Review(rating=5, comment="The definitive reference on Python syntax!", book=book1)
        rev2 = Review(rating=4, comment="Very insightful, advanced dive into CPython.", book=book2)

        # Create Book linked to Martin
        book3 = Book(title="Refactoring: Improving Code Design", isbn="978-0201485677", price=49.99, author=martin)
        rev3 = Review(rating=5, comment="Essential reading for every senior engineer.", book=book3)

        session.add_all([guido, martin])
        session.commit()
        print("Seeded authors, books, and reviews successfully into SQLite.")

    # 3. Modern Queries: select() and scalars()
    section("2. Modern SQLAlchemy 2.0 select() Queries")
    with Session(engine) as session:
        # Simple query with filter
        stmt = select(Book).where(Book.price >= 45.0).order_by(Book.price.desc())
        expensive_books = session.scalars(stmt).all()

        print("Books costing $45.00 or more:")
        for b in expensive_books:
            print(f"  - {b.title:<35} | ${b.price:.2f} (Author ID: {b.author_id})")

    # 4. Eager Loading (preventing N+1 queries)
    section("3. Eager Loading Relationships (selectinload)")
    with Session(engine) as session:
        # Eagerly load books and their reviews in optimized batches
        stmt = select(Author).options(
            selectinload(Author.books).selectinload(Book.reviews)
        )
        authors = session.scalars(stmt).all()

        for a in authors:
            print(f"\nAuthor: {a.name} ({a.email})")
            for b in a.books:
                print(f"   📘 {b.title} (${b.price:.2f})")
                for r in b.reviews:
                    print(f"      ⭐ {r.rating}/5 stars: \"{r.comment}\"")

    # 5. Joins and Aggregations
    section("4. SQL Joins & Aggregate Functions")
    with Session(engine) as session:
        stmt = (
            select(
                Author.name,
                func.count(Book.id).label("book_count"),
                func.avg(Book.price).label("avg_price"),
            )
            .join(Author.books)
            .group_by(Author.id)
            .order_by(func.count(Book.id).desc())
        )
        stats = session.execute(stmt).all()

        print(f"{'Author Name':<22} | {'Books Published':<16} | {'Avg Price':<10}")
        print("-" * 55)
        for name, count, avg_p in stats:
            print(f"{name:<22} | {count:<16} | ${avg_p:.2f}")

    # 6. Cascade Delete
    section("5. Cascade Deletions (cascade='all, delete-orphan')")
    with Session(engine) as session:
        guido_author = session.scalars(select(Author).where(Author.name == "Guido van Rossum")).one()
        print(f"Deleting author '{guido_author.name}'...")
        session.delete(guido_author)
        session.commit()

        # Verify books and reviews were automatically deleted
        remaining_books = session.scalars(select(Book)).all()
        remaining_reviews = session.scalars(select(Review)).all()
        print(f"Remaining books in database:   {len(remaining_books)}")
        print(f"Remaining reviews in database: {len(remaining_reviews)}")
        print("Cascade deletion successfully pruned orphan records.")

    print("\n✅ Part 13 execution complete!")


if __name__ == "__main__":
    run_demonstration()
