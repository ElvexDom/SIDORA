from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from application.models.entities import *


class DatabaseManager:
    """
    Gestionnaire de la base de données SQLite avec SQLAlchemy.
    Fournit les opérations CRUD et l'initialisation de la base.
    """

    def __init__(self, db_path: str = "application/data/db_games.db"):
        """
        Initialise le moteur SQLAlchemy et la session.
        Crée le dossier de la base si nécessaire.
        """
        self.DB_PATH = Path(db_path)
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.DB_URL = f"sqlite:///{self.DB_PATH}"

        # Création du moteur et de la session
        self.engine = create_engine(self.DB_URL, echo=False)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def exists(self) -> bool:
        """Retourne True si la base existe déjà."""
        return self.DB_PATH.exists()

    def initialize(self, csv_path: str | None = None):
        """
        Initialise la base de données :
        - Crée toutes les tables si elles n'existent pas.
        - Insère des données depuis un CSV si fourni.
        """
        from application.services.game_services import read_csv_to_df, generate_and_insert_games, generate_fake_users_with_games

        try:
            # Création des tables
            Base.metadata.create_all(self.engine)
            print(f"[INFO] {len(Base.metadata.tables)} tables ont été créées avec succès.")

            # Insertion des données si CSV fourni
            if csv_path:
                df_games = read_csv_to_df(csv_path)
                with self.Session() as session:
                    try:
                        session.add(Genre(name="Unknown"))
                        session.add(Publisher(name="Unknown"))
                        generate_and_insert_games(session, df_games)
                        generate_fake_users_with_games(session, num_users=50)
                        session.commit()
                        print("[INFO] Données insérées avec succès.")
                    except SQLAlchemyError as e:
                        session.rollback()
                        print(f"[ERROR] Erreur SQLAlchemy lors de l'insertion des données : {e}")
                        raise  # remonter l'erreur si nécessaire
            print("[INFO] Initialisation de la base terminée avec succès.")
        except Exception as e:
            print(f"[ERROR] Erreur inattendue lors de l'initialisation de la DB : {e}")
            raise

    # ------------------------ CRUD ------------------------

    def store_models(self, models: object | list[object]) -> list[object]:
        """
        Insère un ou plusieurs objets dans la base.
        Retourne la liste des objets insérés ou une liste vide en cas d'erreur.
        """
        if not models:
            raise ValueError("Aucun modèle à insérer dans la base")

        if not isinstance(models, list):
            models = [models]

        with self.Session() as session:
            try:
                session.add_all(models)
                session.commit()
                return models
            except SQLAlchemyError as e:
                session.rollback()
                print(f"[ERROR] Erreur SQLAlchemy lors de l'insertion : {e}")
                return []

    def fetch_model(self, model: object, filters: dict | None = None, first: bool = False) -> object | list[object] | None:
        """
        Lit des objets depuis la table du modèle fourni.
        - filters : dictionnaire des filtres à appliquer (optionnel)
        - first : si True, retourne le premier objet trouvé
        """
        if not model:
            raise ValueError("Aucun modèle à lire dans la base")

        try:
            with self.Session() as session:
                query = session.query(model)
                if filters:
                    query = query.filter_by(**filters)
                return query.first() if first else query.all()
        except SQLAlchemyError as e:
            print(f"[ERROR] Erreur SQLAlchemy lors de la lecture de {model.__name__}: {e}")
            return None

    def update_model(self, model: object, filters: dict, values: dict) -> int | None:
        """
        Met à jour des objets correspondant aux filtres avec les valeurs fournies.
        Retourne le nombre de lignes mises à jour ou None en cas d'erreur.
        """
        if not model or not filters or not values:
            raise ValueError("Modèle, filtres et valeurs sont requis pour la mise à jour")

        with self.Session() as session:
            try:
                query = session.query(model).filter_by(**filters)
                updated_count = query.update(values, synchronize_session="fetch")
                session.commit()
                print(f"[INFO] {updated_count} ligne(s) mise(s) à jour dans la table {model.__name__}.")
                return updated_count
            except SQLAlchemyError as e:
                session.rollback()
                print(f"[ERROR] Erreur SQLAlchemy lors de la mise à jour de {model.__name__}: {e}")
                return None

    def delete_model(self, model: object, filters: dict) -> int | None:
        """
        Supprime les objets correspondant aux filtres fournis.
        Retourne le nombre de lignes supprimées ou None en cas d'erreur.
        """
        if not model or not filters:
            raise ValueError("Modèle et filtres sont requis pour la suppression")

        with self.Session() as session:
            try:
                query = session.query(model).filter_by(**filters)
                deleted_count = query.delete(synchronize_session="fetch")
                session.commit()
                print(f"[INFO] {deleted_count} ligne(s) supprimée(s) dans la table {model.__name__}.")
                return deleted_count
            except SQLAlchemyError as e:
                session.rollback()
                print(f"[ERROR] Erreur SQLAlchemy lors de la suppression dans {model.__name__}: {e}")
                return None
