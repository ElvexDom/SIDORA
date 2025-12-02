from application.db.database_manager import DatabaseManager
from application.utils.log_watcher import LogWatcher

CSV_PATH = "application/data/vgsales.csv"

def start():
    """
    Fonction principale pour démarrer l'application.
    Vérifie si la base existe, sinon l'initialise.
    """
    LogWatcher.log("info", "Démarrage de l'application.", True)
    # Création de l'instance du gestionnaire de base
    db = DatabaseManager()
    if not db.exists():
        LogWatcher.log("info", "Début de l'initialisation de la base de données", True)
        try:
            db.initialize(CSV_PATH)
            LogWatcher.log("info", "Initialisation de la base terminée avec succès.", True)
        except Exception as e:
            LogWatcher.log("critical", f"Impossible d'initialiser la base : {e}", True)
            return
    else:
        LogWatcher.log("info", "Base de données existante: aucune action nécessaire.", True)

    # Fermer le moteur proprement
    db.engine.dispose()
    LogWatcher.log("info", "Fermeture de l'application.", True)

if __name__ == "__main__":
    start()
