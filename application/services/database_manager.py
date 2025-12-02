from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from application.models.entities import Base, Genre, Publisher
from application.utils.data_seeder import DataSeeder
from application.utils.log_watcher import LogWatcher


class DatabaseManager:
    """
    Gestionnaire centralisé de la base de données SQLite avec SQLAlchemy.

    Cette classe fournit :
        - L'initialisation de la base avec création de tables et insertion de données.
        - Des méthodes CRUD génériques pour insérer, lire, mettre à jour et supprimer des modèles.
        - La gestion des sessions SQLAlchemy et des exceptions SQLAlchemy.

    Attributs
    ---------
    DB_PATH : Path
        Chemin vers le fichier de la base de données SQLite.
    DB_URL : str
        URL SQLAlchemy pour la connexion à la base.
    engine : Engine
        Moteur SQLAlchemy pour les opérations sur la base.
    Session : sessionmaker
        Fabrique de sessions SQLAlchemy.
    """

    DB_PATH: Path
    DB_URL: str
    engine: Engine
    Session: sessionmaker

    def __init__(self, db_path: str) -> None:
        """
        Initialise le gestionnaire de la base de données.

        Parameters
        ----------
        db_path : str
            Chemin vers le fichier SQLite. Crée le dossier parent si nécessaire.
        """
        self.DB_PATH = Path(db_path)
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.DB_URL = f"sqlite:///{self.DB_PATH}"

        self.engine = create_engine(self.DB_URL, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def exists(self) -> bool:
        """
        Vérifie si le fichier de base de données existe.

        Returns
        -------
        bool
            True si la base existe, False sinon.
        """
        return self.DB_PATH.exists()

    def initialize(self, csv_path: str = None) -> None:
        """
        Initialise la base de données :
            - Création des tables.
            - Insertion des valeurs par défaut (Genre et Publisher "Unknown").
            - Insertion des jeux depuis un CSV si fourni.
            - Génération d'utilisateurs factices avec jeux associés.

        Parameters
        ----------
        csv_path : str, optional
            Chemin vers le fichier CSV pour insérer des jeux.

        Raises
        ------
        SQLAlchemyError
            Si une erreur SQLAlchemy se produit lors de l'initialisation.
        Exception
            Pour toute autre erreur inattendue.
        """
        try:
            Base.metadata.create_all(self.engine)
            LogWatcher.log("info", f"{len(Base.metadata.tables)} tables créées avec succès.")

            with self.Session() as session:
                data_seeder = DataSeeder(session)

                session.add_all([
                    Genre(name="Unknown"),
                    Publisher(name="Unknown")
                ])

                if csv_path:
                    data_seeder.read_and_insert_games(csv_path)
                data_seeder.generate_fake_users_with_games()

                session.commit()
                LogWatcher.log("info", "Données insérées avec succès.")
        except SQLAlchemyError as e:
            LogWatcher.log("error", f"Erreur SQLAlchemy lors de l'initialisation: {e}", True)
            raise
        except Exception as e:
            LogWatcher.log("critical", f"Erreur inattendue lors de l'initialisation de la DB: {e}", True)
            raise

    # ------------------------ CRUD ------------------------

    def store_models(self, models: object | list[object]) -> list[object]:
        """
        Insère un ou plusieurs modèles dans la base.

        Parameters
        ----------
        models : object ou list[object]
            Un modèle SQLAlchemy ou une liste de modèles à insérer.

        Returns
        -------
        list[object]
            Liste des modèles insérés avec succès.

        Raises
        ------
        ValueError
            Si aucun modèle n'est fourni.
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
                LogWatcher.log("error", f"Erreur SQLAlchemy lors de l'insertion: {e}", True)
                return []

    def fetch_model(self, model: object, filters: dict = None, first: bool = False) -> object | list[object] | None:
        """
        Récupère un ou plusieurs modèles depuis la base.

        Parameters
        ----------
        model : object
            Le modèle SQLAlchemy à récupérer.
        filters : dict, optional
            Dictionnaire de filtres à appliquer (équivalent de filter_by).
        first : bool, optional
            Si True, retourne uniquement le premier résultat.

        Returns
        -------
        object ou list[object] ou None
            Les résultats correspondant aux filtres ou None en cas d'erreur.

        Raises
        ------
        ValueError
            Si le modèle est None.
        """
        if not model:
            raise ValueError("Aucun modèle à lire dans la base")

        with self.Session() as session:
            try:
                query = session.query(model)
                if filters:
                    query = query.filter_by(**filters)
                return query.first() if first else query.all()
            except SQLAlchemyError as e:
                LogWatcher.log("error", f"Erreur SQLAlchemy lors de la lecture de {model.__name__}: {e}", True)
                return None

    def update_model(self, model: object, filters: dict, values: dict) -> int | None:
        """
        Met à jour des enregistrements dans la base.

        Parameters
        ----------
        model : object
            Le modèle SQLAlchemy à mettre à jour.
        filters : dict
            Dictionnaire de filtres pour sélectionner les lignes à mettre à jour.
        values : dict
            Dictionnaire des nouvelles valeurs à appliquer.

        Returns
        -------
        int ou None
            Nombre de lignes mises à jour ou None en cas d'erreur.

        Raises
        ------
        ValueError
            Si modèle, filtres ou valeurs manquent.
        """
        if not model or not filters or not values:
            raise ValueError("Modèle, filtres et valeurs sont requis pour la mise à jour")

        with self.Session() as session:
            try:
                query = session.query(model).filter_by(**filters)
                updated_count = query.update(values, synchronize_session="fetch")
                session.commit()
                LogWatcher.log("info", f"{updated_count} ligne(s) mise(s) à jour dans {model.__name__}.")
                return updated_count
            except SQLAlchemyError as e:
                session.rollback()
                LogWatcher.log("error", f"Erreur SQLAlchemy lors de la mise à jour de {model.__name__}: {e}", True)
                return None

    def delete_model(self, model: object, filters: dict) -> int | None:
        """
        Supprime des enregistrements dans la base.

        Parameters
        ----------
        model : object
            Le modèle SQLAlchemy dont les lignes doivent être supprimées.
        filters : dict
            Dictionnaire de filtres pour sélectionner les lignes à supprimer.

        Returns
        -------
        int ou None
            Nombre de lignes supprimées ou None en cas d'erreur.

        Raises
        ------
        ValueError
            Si modèle ou filtres manquent.
        """
        if not model or not filters:
            raise ValueError("Modèle et filtres sont requis pour la suppression")

        with self.Session() as session:
            try:
                query = session.query(model).filter_by(**filters)
                deleted_count = query.delete(synchronize_session="fetch")
                session.commit()
                LogWatcher.log("info", f"{deleted_count} ligne(s) supprimée(s) dans {model.__name__}.")
                return deleted_count
            except SQLAlchemyError as e:
                session.rollback()
                LogWatcher.log("error", f"Erreur SQLAlchemy lors de la suppression dans {model.__name__}: {e}", True)
                return None
