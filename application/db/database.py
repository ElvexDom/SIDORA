from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.models.entities import Base  # pour créer les tables

# Création du moteur SQLite
engine = create_engine("sqlite:///application/data/db_games.db", echo=False)

# Création des tables si elles n'existent pas
Base.metadata.create_all(engine)

# Fabrique de sessions
Session = sessionmaker(bind=engine)
