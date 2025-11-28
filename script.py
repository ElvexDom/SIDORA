from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError # Pour la gestion des erreurs

# --- 1. DÉFINITION DES MODÈLES (Base MERISE/MLD) ---
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    nom = Column(String)
    # Relation 1-N : un Client a plusieurs Commandes
    commandes = relationship("Commande", back_populates="client", cascade="all, delete-orphan") 
    # Ajout de 'cascade' pour garantir la suppression des commandes si le client est supprimé.

    def __repr__(self):
        return f"Client(id={self.id}, nom='{self.nom}')"

class Commande(Base):
    __tablename__ = 'commandes'
    id = Column(Integer, primary_key=True)
    montant = Column(Integer)
    # Clé étrangère vers la table 'clients'
    client_id = Column(Integer, ForeignKey('clients.id'))
    # Relation N-1 : une Commande appartient à un Client
    client = relationship("Client", back_populates="commandes")

    def __repr__(self):
        return f"Commande(id={self.id}, montant={self.montant}, client_id={self.client_id})"

# --- 2. INITIALISATION ET CONNEXION À LA BASE ---

# Crée le moteur (connexion SQLite dans un fichier 'ecom.db')
engine = create_engine("sqlite:///ecom.db", echo=False) # echo=True pour voir le SQL

# Crée les tables si elles n'existent pas encore
Base.metadata.create_all(engine)

# Crée la fabrique de sessions (la 'recette' pour créer des sessions)
Session = sessionmaker(bind=engine)

# --- 3. FONCTION D'EXÉCUTION ET GESTION DE LA TRANSACTION ---

def executer_transaction():
    print("--- Démarrage de la transaction ---")
    
    # Le bloc 'with' garantit la fermeture de la session, 
    # même en cas d'erreur.
    try:
        # 1. Création de la session (entre dans le bloc 'with')
        with Session() as session:
            # Création des nouveaux objets
            client_neo = Client(nom="Neo")
            client_trinity = Client(nom="Trinity")
            
            # Neo passe deux commandes
            client_neo.commandes.extend([
                Commande(montant=120),
                Commande(montant=25)
            ])
            
            # Ajout des deux clients (et de leurs commandes liées)
            session.add_all([client_neo, client_trinity])
            
            # Exécution des INSERTs SQL
            session.commit()
            print("Client et commandes insérés avec succès.")
            
            # --- Exemple de lecture après insertion ---
            
            # Lecture de toutes les commandes du client "Neo"
            commandes_neo = (
                session.query(Commande)
                .filter(Commande.client_id == client_neo.id)
                .all()
            )
            print(f"\nCommandes de {client_neo.nom} :")
            for cmd in commandes_neo:
                print(f"  - ID Commande: {cmd.id}, Montant: {cmd.montant}")

    except SQLAlchemyError as e:
        # Si une erreur se produit (par exemple, si la BDD est inaccessible), 
        # le 'rollback' est exécuté.
        session.rollback() 
        print(f"\n❌ ERREUR DE TRANSACTION : Opération annulée. Détail: {e}")
        
    finally:
        # La session est automatiquement fermée après le bloc 'with'.
        print("\n--- Fin de la transaction (Session fermée) ---")


# --- 4. EXÉCUTION ET NETTOYAGE FINAL ---
if __name__ == "__main__":
    executer_transaction()
    
    # Fermeture définitive du pool de connexions du moteur
    engine.dispose()
    print("Ressources du moteur libérées.")