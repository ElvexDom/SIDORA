from datetime import date
import pytest
from typing import Generator

from application.services.database_manager import DatabaseManager
from application.utils.crypto_tools import CryptoTools
from application.models.entities import Base, User


# ----------------------------
# Fixture pytest : DatabaseManager en mémoire
# ----------------------------
@pytest.fixture
def db_manager() -> Generator[DatabaseManager, None, None]:
    """
    Fixture pour créer un DatabaseManager en mémoire SQLite.
    
    Returns
    -------
    DatabaseManager
        Instance de DatabaseManager connectée à une base en mémoire.
    """
    manager = DatabaseManager(db_path=":memory:")
    Base.metadata.create_all(manager.engine)
    yield manager


# ----------------------------
# Tests CRUD pour User
# ----------------------------

def test_store_and_fetch_user(db_manager: DatabaseManager) -> None:
    """
    Teste l'insertion et la récupération d'un utilisateur.
    Vérifie que l'utilisateur est correctement stocké et récupéré.
    """
    email: str = "alice@example.com"
    user: User = User(
        pseudo="Alice",
        password=CryptoTools.hash_password("monMotDePasse123"),
        mail=CryptoTools.hash_email(email),
        consent=True,
        expiry=date(2025, 12, 31)
    )

    stored: list[User] = db_manager.store_models(user)
    assert len(stored) == 1

    fetched: User | None = db_manager.fetch_model(User, {"pseudo": "Alice"}, first=True)
    assert fetched is not None
    assert fetched.mail == CryptoTools.hash_email(email)


def test_update_user(db_manager: DatabaseManager) -> None:
    """
    Teste la mise à jour d'un utilisateur existant.
    Vérifie que le pseudo est correctement modifié.
    """
    email: str = "bob@example.com"
    user: User = User(
        pseudo="Bob",
        password=CryptoTools.hash_password("monMotDePasse123"),
        mail=CryptoTools.hash_email(email),
        consent=True,
        expiry=date(2025, 12, 31)
    )

    db_manager.store_models(user)

    updated_count: int | None = db_manager.update_model(User, {"pseudo": "Bob"}, {"pseudo": "Robert"})
    assert updated_count == 1

    fetched: User | None = db_manager.fetch_model(User, {"pseudo": "Robert"}, first=True)
    assert fetched is not None
    assert fetched.mail == CryptoTools.hash_email(email)


def test_delete_user(db_manager: DatabaseManager) -> None:
    """
    Teste la suppression d'un utilisateur.
    Vérifie que l'utilisateur n'existe plus après la suppression.
    """
    email: str = "charlie@example.com"
    user: User = User(
        pseudo="Charlie",
        password=CryptoTools.hash_password("monMotDePasse123"),
        mail=CryptoTools.hash_email(email),
        consent=True,
        expiry=date(2025, 12, 31)
    )

    db_manager.store_models(user)

    deleted_count: int | None = db_manager.delete_model(User, {"pseudo": "Charlie"})
    assert deleted_count == 1

    fetched: list[User] = db_manager.fetch_model(User, {"pseudo": "Charlie"})
    assert fetched == []
