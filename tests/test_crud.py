import sys
from datetime import date
from pathlib import Path
import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from application.db.database_manager import DatabaseManager
from application.utils.crypto_tools import CryptoTools
from application.models.entities import Base, User

# ----------------------------
# Fixture pytest : DatabaseManager en mémoire
# ----------------------------
@pytest.fixture
def db_manager():
    manager = DatabaseManager(db_path=":memory:")
    Base.metadata.create_all(manager.engine)
    return manager

# ----------------------------
# Tests CRUD pour User
# ----------------------------

def test_store_and_fetch_user(db_manager):
    email = "alice@example.com"
    user = User(
        pseudo="Alice",
        password=CryptoTools.hash_password("monMotDePasse123"),
        mail=CryptoTools.hash_email(email),
        consent=True,
        expiry=date(2025, 12, 31)
    )
    stored = db_manager.store_models(user)
    assert len(stored) == 1

    fetched = db_manager.fetch_model(User, {"pseudo": "Alice"}, first=True)
    assert fetched.mail == CryptoTools.hash_email(email)

def test_update_user(db_manager):
    email = "bob@example.com"
    user = User(
        pseudo="Bob",
        password=CryptoTools.hash_password("monMotDePasse123"),
        mail=CryptoTools.hash_email(email),
        consent=True,
        expiry=date(2025, 12, 31)
    )
    db_manager.store_models(user)

    updated_count = db_manager.update_model(User, {"pseudo": "Bob"}, {"pseudo": "Robert"})
    assert updated_count == 1

    fetched = db_manager.fetch_model(User, {"pseudo": "Robert"}, first=True)
    assert fetched.mail == CryptoTools.hash_email(email)

def test_delete_user(db_manager):
    email = "charlie@example.com"
    user = User(
        pseudo="Charlie",
        password=CryptoTools.hash_password("monMotDePasse123"),
        mail=CryptoTools.hash_email(email),
        consent=True,
        expiry=date(2025, 12, 31)
    )
    db_manager.store_models(user)

    deleted_count = db_manager.delete_model(User, {"pseudo": "Charlie"})
    assert deleted_count == 1

    fetched = db_manager.fetch_model(User, {"pseudo": "Charlie"})
    assert fetched == []
