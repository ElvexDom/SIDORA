from application.services.database_manager import DatabaseManager
from application.utils.log_watcher import LogWatcher
from sqlalchemy.engine import Engine

DB_PATH: str = "application/database/sidora.db"
CSV_PATH: str = "application/data/vgsales.csv"


class Application:
    """
    Classe principale pour gérer le cycle de vie de l'application SIDORA.

    Cette classe se charge de :
        - Vérifier l'existence de la base de données.
        - Initialiser la base de données si elle n'existe pas, en utilisant un CSV fourni.
        - Fermer proprement le moteur SQLAlchemy lors de l'arrêt.

    Attributs
    ---------
    db : DatabaseManager
        Instance de DatabaseManager pour gérer la base de données.
    csv_path : str
        Chemin vers le fichier CSV contenant les données à insérer.
    """

    db: DatabaseManager
    csv_path: str

    def __init__(self, db_path: str = DB_PATH, csv_path: str = CSV_PATH) -> None:
        """
        Initialise l'application.

        Parameters
        ----------
        db_path : str, optional
            Chemin vers le fichier de base de données SQLite (par défaut DB_PATH).
        csv_path : str, optional
            Chemin vers le fichier CSV à utiliser pour l'initialisation (par défaut CSV_PATH).
        """
        self.csv_path: str = csv_path
        self.db: DatabaseManager = DatabaseManager(db_path)

    def run(self) -> None:
        """
        Démarre l'application.

        Cette méthode effectue les opérations suivantes :
            - Log le démarrage de l'application.
            - Vérifie si la base de données existe.
            - Si la base n'existe pas, l'initialise avec le CSV fourni.
            - Log les différentes étapes et les erreurs éventuelles.
            - Ferme proprement le moteur SQLAlchemy à la fin.

        Raises
        ------
        Exception
            Si l'initialisation de la base échoue, l'exception est loggée et propagée.
        """
        LogWatcher.log("info", "Démarrage de l'application.", True)

        try:
            if not self.db.exists():
                LogWatcher.log("info", "Début de l'initialisation de la base de données", True)
                try:
                    self.db.initialize(self.csv_path)
                    LogWatcher.log("info", "Initialisation de la base terminée avec succès.", True)
                except Exception as e:
                    LogWatcher.log("critical", f"Impossible d'initialiser la base : {e}", True)
                    return
            else:
                LogWatcher.log("info", "Base de données existante : aucune action nécessaire.", True)

        finally:
            # Fermer proprement le moteur SQLAlchemy 2.x
            engine: Engine = self.db.engine
            engine.dispose()
            LogWatcher.log("info", "Fermeture de l'application.", True)


if __name__ == "__main__":
    app: Application = Application()
    app.run()
