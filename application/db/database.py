from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from application.models.entities import *
from application.utils.utils import generate_fake_users

# -------------------------------------------------------------------
# Chemin vers la base SQLite
# -------------------------------------------------------------------
DB_PATH = Path("application/data/db_games.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Crée le dossier si nécessaire
DB_URL = f"sqlite:///{DB_PATH}"
csv_path = "application/data/vgsales.csv"

# -------------------------------------------------------------------
# Création du moteur et de la session SQLAlchemy
# -------------------------------------------------------------------
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

# -------------------------------------------------------------------
# Vérification de l'existence de la base
# -------------------------------------------------------------------
def db_exists() -> bool:
    """Retourne True si le fichier de la base SQLite existe."""
    return DB_PATH.exists()

# -------------------------------------------------------------------
# Initialisation de la base et insertion des utilisateurs Faker
# -------------------------------------------------------------------
def init_db(num_users=50):
    """
    Crée toutes les tables si elles n'existent pas
    et insère des utilisateurs générés par Faker.
    """
    # Création de toutes les tables définies dans Base.metadata
    Base.metadata.create_all(engine)
    print("[INFO] Toutes les tables ont été créées si nécessaire.")

    create([Genre(name="Unknown")], session)
    create([Publisher(name="Unknown")], session)
    # null_platform = create([Platform(id=0, name=None)])
    # null_publisher = create([Publisher(id=0, name=None)])

    # Génération des utilisateurs Faker
    # users = generate_fake_users(num_users)

    # Insertion dans la table correspondante
    # create(users, session)

    # --------------------------
    # Génération des tables jeux et associées
    # --------------------------
    if csv_path:
        from application.utils.utils import read_csv_to_df, generate_and_insert_games, generate_fake_users_with_games

        # Conversion CSV ou liste dict -> DataFrame
        df_games = read_csv_to_df(csv_path)

        # Génération des objets ORM
        generate_and_insert_games(df_games, session)

        generate_fake_users_with_games(session, num_users=50)


# -------------------------------------------------------------------
# Fonction générique d'insertion
# -------------------------------------------------------------------
def create(entries: list, session):
    """
    Insère des entrées dans la base.

    Args:
        entries (list): liste d'objets ORM à insérer.
    """
    if not entries:
        print("[INFO] Aucune entrée à insérer.")
        return

    # session = Session()
    try:
        session.add_all(entries)  # SQLAlchemy détecte automatiquement la table via les instances
        session.commit()
        print(f"[INFO] {len(entries)} entrées insérées avec succès.")
        return entries
    except SQLAlchemyError as e:
        session.rollback()
        print(f"[ERROR] Erreur lors de l'insertion : {e}")
    finally:
        session.close()

def read(model, filters: dict | None = None, first: bool = False):
    """
    Lit des données depuis une table SQLAlchemy.

    Args:
        model: classe SQLAlchemy (ex: User, Genre, Game)
        filters (dict): filtres optionnels {champ: valeur}
        first (bool): True → retourne un seul objet, False → une liste

    Returns:
        Objet ou liste d'objets SQLAlchemy
    """
    session = Session()
    try:
        query = session.query(model)

        if filters:
            query = query.filter_by(**filters)

        result = query.first() if first else query.all()
        return result

    finally:
        session.close()