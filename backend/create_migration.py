#!/usr/bin/env python
"""Generate initial Alembic migration from SQLAlchemy models."""
import os
import sys
from alembic.config import Config
from alembic.command import revision

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from app.core.db import Base
from app.models.product import Producto
from app.models.venta import Venta

if __name__ == '__main__':
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), 'alembic.ini'))
    
    # Auto-generate migration
    revision(alembic_cfg, autogenerate=True, message="Initial migration from models")
    print("Migration created. Run 'alembic upgrade head' to apply.")
