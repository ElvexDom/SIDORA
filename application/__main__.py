from application.db.database import engine, init_db, db_exists

def start():
    """
    Fonction principale pour démarrer l'application.
    Vérifie si la base existe, sinon l'initialise.
    """
    if not db_exists():
        print("Base de données non trouvée, initialisation...")
        init_db()
    else:
        print("Base de données existante, aucune action nécessaire.")

    # Ici tu peux démarrer ton application ou exécuter d'autres fonctions

    engine.dispose()


if __name__ == "__main__":
    start()
