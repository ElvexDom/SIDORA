from application.db.database_manager import DatabaseManager

CSV_PATH = "application/data/vgsales.csv"

def start():
    """
    Fonction principale pour démarrer l'application.
    Vérifie si la base existe, sinon l'initialise.
    """
    # Création de l'instance du gestionnaire de base
    db = DatabaseManager()

    if not db.exists():
        print("[INFO] Initialisation de la base de données...")
        try:
            db.initialize(CSV_PATH)
        except Exception as e:
            print(f"[ERROR] Impossible d'initialiser la base : {e}")
            return
    else:
        print("[INFO] Base de données existante, aucune action nécessaire.")

    # Fermer le moteur proprement
    db.engine.dispose()
    print("[INFO] Application terminée.")


if __name__ == "__main__":
    start()
