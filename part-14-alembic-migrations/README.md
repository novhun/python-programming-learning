

# Part 14: Database Schema Migrations with Alembic

In real-world applications, database schemas evolve constantly. You need to add tables, rename columns, create indices, and alter data constraints over time. Dropping and recreating tables in production is not an option.

**Alembic** is the premier database migration framework for SQLAlchemy, enabling version-controlled, reproducible schema migrations across development, staging, and production environments.

---

## 📖 Key Concepts & Architecture

### 1. Anatomy of an Alembic Environment

When you run `alembic init alembic`, it generates:

- **`alembic.ini`**: Configuration file containing database URL, logging settings, and script paths.
- **`alembic/env.py`**: A Python script executed whenever the migration tool runs. It connects Alembic to your SQLAlchemy `Base.metadata`.
- **`alembic/script.py.mako`**: Template file used to generate new migration scripts.
- **`alembic/versions/`**: Directory containing individual revision files.

### 2. Migration Revisions (`upgrade()` and `downgrade()`)

Each migration script defines two fundamental functions:

```python
"""add status column to users

Revision ID: 002_add_status
Revises: 001_initial
Create Date: 2026-10-28
"""
from alembic import op
import sqlalchemy as sa

revision = '002_add_status'
down_revision = '001_initial'

def upgrade():
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False))

def downgrade():
    op.drop_column('users', 'is_active')
```

### 3. Essential CLI Commands

| Command                                          | Description                                                            |
| :----------------------------------------------- | :--------------------------------------------------------------------- |
| `alembic init <dir>`                           | Initializes a new migration environment                                |
| `alembic revision -m "message"`                | Generates a blank revision file                                        |
| `alembic revision --autogenerate -m "message"` | Compares SQLAlchemy models against DB and drafts changes automatically |
| `alembic upgrade head`                         | Runs all pending migrations up to the latest revision                  |
| `alembic downgrade -1`                         | Rolls back the most recent migration                                   |
| `alembic current`                              | Displays the current database revision ID                              |
| `alembic history --verbose`                    | Displays the full chronological migration chain                        |

---

## 🏃‍♂️ How to Run the Code

### 1. Install Dependencies

```bash
pip install -r part-14-alembic-migrations/requirements.txt
```

### 2. Run the Programmatic Migration Demonstration

The accompanying `main.py` demonstrates how to invoke Alembic programmatically in Python, applying migrations, rolling them back, and inspecting table schemas:

```bash
python3 part-14-alembic-migrations/main.py
```

---

## ✍️ Practice Exercises

1. **Auto-generation Workflow**: Modify a model in `models.py` by adding a new column (e.g. `bio = Column(Text)`). Run `alembic revision --autogenerate -m "add bio column"` and examine the generated Python file in `alembic/versions/`.
2. **Data Migration**: Write a revision where `upgrade()` not only alters a column, but also populates default data into existing rows using `op.bulk_insert()`.
3. **Rollback Safety**: Test running `alembic upgrade head`, inserting test data, running `alembic downgrade -1`, and verifying that down revisions preserve data integrity where applicable.
