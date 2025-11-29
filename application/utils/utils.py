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
    
    Seuls les utilisateurs avec consentement sont stockés.
    Expiry définit la durée de conservation pour conformité RGPD.
    """
    users = []

    for _ in range(num_users):
        consent = fake.boolean(chance_of_getting_true=80)  # 80% de consentement simulé
        if not consent:
            continue  # Ne pas stocker les données si consentement False

        raw_password = fake.password(length=10)
        raw_mail = fake.unique.email()  # donnée sensible fictive

        user = User(
            pseudo=fake.unique.user_name(),
            password=hash_password(raw_password),
            mail=hash_email(raw_mail),
            consent=True,
            expiry=fake.date_between(start_date="today", end_date="+5y")
        )
        users.append(user)

    return users
