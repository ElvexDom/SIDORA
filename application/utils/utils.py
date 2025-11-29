from pathlib import Path
import hashlib
import bcrypt
from faker import Faker
from application.models.entities import User

fake = Faker()

def hash_password(password: str) -> str:
    """
    Hash sécurisé du mot de passe avec bcrypt.
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def hash_email(email: str) -> str:
    """
    Anonymisation de l'email par SHA-256.
    Non réversible, peut seulement être utilisé pour vérification/unicité.
    """
    normalized = email.strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def generate_fake_users(num_users=50):
    """
    Génère des utilisateurs avec :
    - mot de passe hashé (bcrypt)
    - email anonymisé (SHA-256)
    """
    users = []

    for _ in range(num_users):
        raw_password = fake.password(length=10)
        raw_email = fake.unique.email()

        user = User(
            pseudo=fake.unique.user_name(),
            password=hash_password(raw_password),
            mail=hash_email(raw_email),
            consent=fake.boolean(chance_of_getting_true=80),
            expiry=fake.date_between(start_date="today", end_date="+5y")
        )
        users.append(user)

    return users
