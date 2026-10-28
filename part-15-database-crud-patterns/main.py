#!/usr/bin/env python3
"""
Part 15: Enterprise Database CRUD & Repository Patterns
--------------------------------------------------------
This runnable script demonstrates:
1. Generic Repository CRUD operations (Create, Read, Update, Delete)
2. Bulk insertion operations
3. Soft Deletion vs Hard Deletion behavior
4. Pagination queries (skip / limit)
5. Unit of Work atomic transaction commit & rollback simulation
"""

from __future__ import annotations
import sys

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from repository import Base, Product, UnitOfWork
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def run_demonstration() -> None:
    if not SQLALCHEMY_AVAILABLE:
        print("=" * 60)
        print("  SQLAlchemy is not installed in the current environment.")
        print("  To run this module, install the dependencies:")
        print("    pip install -r requirements.txt")
        print("  Or:")
        print("    pip install sqlalchemy pydantic")
        print("=" * 60)
        return

    print("╔═══════════════════════════════════════════════════════╗")
    print("║     Part 15: Database CRUD & Repository Patterns      ║")
    print("╚═══════════════════════════════════════════════════════╝")

    # Initialize Engine & Session Factory
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    # 1. CREATE (Single & Bulk)
    section("1. CREATE Operations (Single & Bulk)")
    with UnitOfWork(session_factory) as uow:
        assert uow.products is not None

        # Single item create
        laptop = Product(name="MacBook Pro 16", sku="APL-MBP-16", price=2499.00, stock=15)
        uow.products.add(laptop)

        # Bulk create
        peripherals = [
            Product(name="Mechanical Keyboard", sku="LOG-MX-MECH", price=149.99, stock=45),
            Product(name="Wireless Ergonomic Mouse", sku="LOG-MX-M3", price=99.99, stock=60),
            Product(name="UltraWide Monitor 34-inch", sku="DEL-U3421", price=799.00, stock=8),
            Product(name="USB-C Dual 4K Dock", sku="CAL-DOCK-TS4", price=299.99, stock=20),
        ]
        uow.products.bulk_add(peripherals)
        uow.commit()
        print("Created 5 products successfully via Repository.")

    # 2. READ (Get by ID & Paginated List)
    section("2. READ Operations (Find by ID & Pagination)")
    with UnitOfWork(session_factory) as uow:
        assert uow.products is not None

        # Get by ID
        prod = uow.products.get_by_id(1)
        print(f"Find Product #1: {prod}")

        # Paginated listing (Page 1: 3 items)
        print("\nPaginated Query (skip=0, limit=3):")
        page_1 = uow.products.list(skip=0, limit=3)
        for item in page_1:
            print(f"  - {item}")

    # 3. UPDATE Operation
    section("3. UPDATE Operation")
    with UnitOfWork(session_factory) as uow:
        assert uow.products is not None

        print("Applying 10% discount and restocking Product #1 (MacBook Pro):")
        updated = uow.products.update(1, price=2249.10, stock=25)
        uow.commit()
        print(f"After Update: {updated}")

    # 4. SOFT DELETE vs HARD DELETE
    section("4. SOFT DELETE vs HARD DELETE")
    with UnitOfWork(session_factory) as uow:
        assert uow.products is not None

        # Soft Delete Product #2 (Mechanical Keyboard)
        print("Soft deleting Product #2 (LOG-MX-MECH)...")
        uow.products.soft_delete(2)

        # Hard Delete Product #5 (USB-C Dock)
        print("Hard deleting Product #5 (CAL-DOCK-TS4)...")
        uow.products.delete(5)
        uow.commit()

    with UnitOfWork(session_factory) as uow:
        assert uow.products is not None

        print("\nQuerying active products (list() excludes soft-deleted items):")
        active_items = uow.products.list()
        for item in active_items:
            print(f"  ✔ Active: {item}")

        # Verify soft-deleted item still exists in audit query
        soft_deleted = uow.products.get_by_id(2, include_deleted=True)
        print(f"\nAudit query for Product #2 (include_deleted=True):\n  {soft_deleted}")
        print(f"  Deleted timestamp: {soft_deleted.deleted_at if soft_deleted else 'N/A'}")

        # Verify hard-deleted item is completely gone
        hard_deleted = uow.products.get_by_id(5, include_deleted=True)
        print(f"Audit query for Product #5 (Hard Deleted): {hard_deleted} (Permanently purged)")

    # 5. UNIT OF WORK ATOMIC TRANSACTION ROLLBACK
    section("5. Unit of Work Atomic Rollback Simulation")
    try:
        with UnitOfWork(session_factory) as uow:
            assert uow.products is not None
            print("Beginning multi-step transaction...")
            uow.products.add(Product(name="Ghost Product", sku="GHOST-99", price=9.99, stock=1))
            print("  Step 1: Staged new Ghost Product.")

            print("  Step 2: Simulating unexpected payment gateway failure...")
            raise RuntimeError("CRITICAL: Payment service timed out! Aborting transaction.")

            uow.commit()  # Will not be reached
    except RuntimeError as err:
        print(f"  Caught expected error: {err}")
        print("  Unit of Work __exit__ automatically triggered rollback.")

    # Verify Ghost Product was never committed
    with UnitOfWork(session_factory) as uow:
        assert uow.products is not None
        all_now = uow.products.list(include_deleted=True)
        ghost_exists = any(p.sku == "GHOST-99" for p in all_now)
        print(f"Does 'GHOST-99' exist in database? {ghost_exists} -> Atomic consistency preserved!")

    print("\n✅ Part 15 execution complete!")


if __name__ == "__main__":
    run_demonstration()
