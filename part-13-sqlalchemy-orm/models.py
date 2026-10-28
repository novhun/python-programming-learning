"""
SQLAlchemy 2.0 Modern Declarative Models
-----------------------------------------
Demonstrates:
- DeclarativeBase class
- Modern type annotations: Mapped, mapped_column
- One-to-Many and Many-to-One relationships with cascade rules
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # 1 Author -> Many Books
    books: Mapped[list[Book]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
        order_by="Book.title",
    )

    def __repr__(self) -> str:
        return f"<Author id={self.id} name={self.name!r} email={self.email!r}>"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)

    # Many Books -> 1 Author
    author: Mapped[Author] = relationship(back_populates="books")

    # 1 Book -> Many Reviews
    reviews: Mapped[list[Review]] = relationship(
        back_populates="book",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r} price=${self.price:.2f}>"


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 5 stars
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)

    book: Mapped[Book] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review id={self.id} rating={self.rating} stars for book_id={self.book_id}>"
