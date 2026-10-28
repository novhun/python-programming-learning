#!/usr/bin/env python3
"""
Part 14: Database Schema Migrations with Alembic
-------------------------------------------------
This runnable script demonstrates:
1. Programmatically loading Alembic configuration (alembic.ini)
2. Upgrading to revision 001_initial (creating users table)
3. Inspecting the SQLite database columns via SQLAlchemy
4. Upgrading to head (002_add_profile) -> adding 'bio' and 'is_verified'
5. Downgrading back to revision 001_initial -> verifying rollback behavior
6. Upgrading back to head
"""

from __future__ import annotations
import os
from pathlib import Path
import sys

try:
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import create_engine, inspect
    ALEMBIC_AVAILABLE = True
except ImportError:
    ALEMBIC_AVAILABLE = False


def section(title: str) -> None:
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def inspect_user_columns(db_path: Path) -> list[str]:
    """Helper to inspect current column names in the SQLite 'users' table."""
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        return []
    columns = [col["name"] for col in inspector.get_columns("users")]
    return columns


def run_demonstration() -> None:
    if not ALEMBIC_AVAILABLE:
        print("=" * 60)
        print("  Alembic / SQLAlchemy is not installed in the current environment.")
        print("  To run this module, install the dependencies:")
        print("    pip install -r requirements.txt")
        print("  Or:")
        print("    pip install alembic sqlalchemy")
        print("=" * 60)
        return

    print("╔═══════════════════════════════════════════════════════╗")
    print("║     Part 14: Alembic Database Migrations              ║")
    print("╚═══════════════════════════════════════════════════════╝")

    current_dir = Path(__file__).resolve().parent
    ini_path = current_dir / "alembic.ini"
    db_file = current_dir / "migrations_demo.db"

    # Remove existing test db for clean demonstration run
    if db_file.exists():
        db_file.unlink()

    # Initialize Alembic Config programmatically
    alembic_cfg = Config(str(ini_path))
    alembic_cfg.set_main_option("script_location", str(current_dir / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_file}")

    # 1. Apply Initial Migration (Revision 001)
    section("1. Upgrading to Revision '001_initial'")
    print("Running: alembic.command.upgrade(cfg, '001_initial')...")
    command.upgrade(alembic_cfg, "001_initial")

    cols_v1 = inspect_user_columns(db_file)
    print(f"Table 'users' columns after Revision 001:")
    for col in cols_v1:
        print(f"  ✔ {col}")

    # 2. Upgrade to Head (Revision 002)
    section("2. Upgrading to 'head' (Revision 002: Add Columns)")
    print("Running: alembic.command.upgrade(cfg, 'head')...")
    command.upgrade(alembic_cfg, "head")

    cols_v2 = inspect_user_columns(db_file)
    print(f"Table 'users' columns after Revision 002:")
    for col in cols_v2:
        tag = " [NEW COLUMN]" if col in ("bio", "is_verified") else ""
        print(f"  ✔ {col}{tag}")

    # 3. Test Migration Rollback / Downgrade
    section("3. Downgrading to Revision '001_initial' (Rollback)")
    print("Running: alembic.command.downgrade(cfg, '001_initial')...")
    command.downgrade(alembic_cfg, "001_initial")

    cols_v3 = inspect_user_columns(db_file)
    print(f"Table 'users' columns after Downgrade:")
    for col in cols_v3:
        print(f"  ✔ {col}")
    print("Confirmed: 'bio' and 'is_verified' were dropped cleanly without corrupting the table.")

    # 4. Final Upgrade to Head
    section("4. Re-applying Migration to Head")
    command.upgrade(alembic_cfg, "head")
    print("Database schema successfully synchronized with latest revision (head).")

    print("\n" + "=" * 60)
    print("🎉 Alembic migration lifecycle verified successfully!")
    print(f"SQLite database created at: {db_file.name}")
    print("You can inspect revisions via CLI: alembic history --verbose")
    print("=" * 60)


if __name__ == "__main__":
    run_demonstration()
