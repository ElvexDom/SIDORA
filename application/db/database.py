from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from application.models.entities import Base
from application.utils.utils import generate_fake_users

# Chemin vers la base SQLite
DB_PATH = Path("application/data/db_games.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DB_URL = f"sqlite:///{DB_PATH}"

# Création du moteur et de la session
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)

def db_exists() -> bool:
    """Vérifie si le fichier de la base SQLite existe."""
    return DB_PATH.exists()

def init_db(num_users=50):
    """
    Crée toutes les tables si elles n'existent pas
    et insère des utilisateurs Faker dans la table users.
    """
    Base.metadata.create_all(engine)
    print("Toutes les tables ont été créées si nécessaire.")

    session = Session()
    try:
        users = generate_fake_users(num_users)
        session.add_all(users)
        session.commit()
        print(f"{num_users} utilisateurs insérés avec succès dans la table users !")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur lors de l'insertion des utilisateurs : {e}")
    finally:
        session.close()
