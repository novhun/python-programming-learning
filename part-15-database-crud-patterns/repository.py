"""
Enterprise Generic Repository and Unit of Work Patterns
-------------------------------------------------------
Demonstrates:
- Generic CRUD repository: Create, Read, Update, Delete, Soft Delete
- Clean separation between persistence and domain logic
- Unit of Work coordinating atomic transactions
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, Optional, Sequence, Type, TypeVar
from sqlalchemy import Boolean, DateTime, Float, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


# Domain Model with Soft Delete support
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        status = "DELETED" if self.is_deleted else f"${self.price:.2f} (Stock: {self.stock})"
        return f"<Product #{self.id} '{self.name}' ({self.sku}) - {status}>"


T = TypeVar("T", bound=Base)


class IRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> T: ...

    @abstractmethod
    def get_by_id(self, entity_id: int, include_deleted: bool = False) -> T | None: ...

    @abstractmethod
    def list(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> Sequence[T]: ...

    @abstractmethod
    def update(self, entity_id: int, **values: object) -> T | None: ...

    @abstractmethod
    def delete(self, entity_id: int) -> bool: ...

    @abstractmethod
    def soft_delete(self, entity_id: int) -> bool: ...


class SQLAlchemyRepository(IRepository[T]):
    """Generic SQLAlchemy implementation of the Repository Pattern."""

    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        self.session = session
        self.model_cls = model_cls

    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def get_by_id(self, entity_id: int, include_deleted: bool = False) -> T | None:
        stmt = select(self.model_cls).where(getattr(self.model_cls, "id") == entity_id)
        if not include_deleted and hasattr(self.model_cls, "is_deleted"):
            stmt = stmt.where(getattr(self.model_cls, "is_deleted") == False)  # noqa: E712
        return self.session.scalars(stmt).one_or_none()

    def list(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> Sequence[T]:
        stmt = select(self.model_cls)
        if not include_deleted and hasattr(self.model_cls, "is_deleted"):
            stmt = stmt.where(getattr(self.model_cls, "is_deleted") == False)  # noqa: E712
        stmt = stmt.offset(skip).limit(limit)
        return self.session.scalars(stmt).all()

    def update(self, entity_id: int, **values: object) -> T | None:
        entity = self.get_by_id(entity_id)
        if not entity:
            return None
        for key, val in values.items():
            if hasattr(entity, key):
                setattr(entity, key, val)
        return entity

    def delete(self, entity_id: int) -> bool:
        """Hard delete: removes record permanently from database."""
        entity = self.get_by_id(entity_id, include_deleted=True)
        if not entity:
            return False
        self.session.delete(entity)
        return True

    def soft_delete(self, entity_id: int) -> bool:
        """Soft delete: flags record as deleted without dropping rows."""
        entity = self.get_by_id(entity_id)
        if not entity:
            return False
        if hasattr(entity, "is_deleted"):
            setattr(entity, "is_deleted", True)
            if hasattr(entity, "deleted_at"):
                setattr(entity, "deleted_at", datetime.utcnow())
            return True
        return False

    def bulk_add(self, entities: list[T]) -> list[T]:
        self.session.add_all(entities)
        return entities


class UnitOfWork:
    """Manages transactional boundaries and coordinates repositories."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory
        self.session: Session | None = None
        self.products: SQLAlchemyRepository[Product] | None = None

    def __enter__(self) -> UnitOfWork:
        self.session = self.session_factory()
        self.products = SQLAlchemyRepository(self.session, Product)
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        if exc_type is not None:
            self.rollback()
        if self.session:
            self.session.close()

    def commit(self) -> None:
        if self.session:
            self.session.commit()

    def rollback(self) -> None:
        if self.session:
            self.session.rollback()
