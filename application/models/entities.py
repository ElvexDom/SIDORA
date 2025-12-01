from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, CHAR, Float, String, Boolean, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    """
    Modèle représentant un utilisateur de la plateforme.

    Attributs:
        id (Integer): Identifiant unique de l'utilisateur.
        pseudo (String): Pseudonyme de l'utilisateur, unique et obligatoire.
        password (String): Mot de passe de l'utilisateur.
        mail (String): Adresse email unique de l'utilisateur.
        consent (Boolean): Consentement de l'utilisateur (ex: RGPD).
        expiry (Date): Date d'expiration du compte ou du consentement.
        game_links (relationship): Liste des relations GameUser associant l'utilisateur à des jeux.
        linked_games (relationship): Liste des jeux associés à l'utilisateur (via table associative), lecture seule.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    pseudo = Column(String(20), nullable=False, unique=True)
    password = Column(CHAR(60), nullable=False)
    mail = Column(CHAR(64), nullable=False, unique=True)
    consent = Column(Boolean, nullable=False)
    expiry = Column(Date, nullable=False)

    # Relations vers la table associative GameUser
    game_links = relationship("GameUser", back_populates="user", cascade="all, delete-orphan")

    # Relation lecture seule vers les jeux liés
    linked_games = relationship("Game", secondary="games_users", viewonly=True)


class GameUser(Base):
    """
    Table associative représentant la relation many-to-many entre utilisateurs et jeux.

    Attributs:
        user_id (Integer): Clé étrangère vers User.id.
        game_id (Integer): Clé étrangère vers Game.id.
        user (relationship): Relation vers l'utilisateur.
        game (relationship): Relation vers le jeu.
    """

    __tablename__ = "games_users"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)

    user = relationship("User", back_populates="game_links")
    game = relationship("Game", back_populates="user_links")


class Game(Base):
    """
    Modèle représentant un jeu vidéo.

    Attributs:
        id (Integer): Identifiant unique du jeu.
        name (String): Nom du jeu.
        rank (Integer): Classement ou popularité du jeu.
        publisher_id (Integer): Clé étrangère vers Publisher.id.
        genre_id (Integer): Clé étrangère vers Genre.id.
        user_links (relationship): Relations GameUser associant le jeu à des utilisateurs.
        platform_links (relationship): Relations GamePlatform associant le jeu à des plateformes.
        publisher (relationship): Relation vers l'éditeur du jeu.
        genre (relationship): Relation vers le genre du jeu.
        sale (relationship): Relation vers les ventes du jeu.
        linked_users (relationship): Utilisateurs liés au jeu (lecture seule).
        linked_platforms (relationship): Plateformes liées au jeu (lecture seule).
    """

    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    rank = Column(Integer, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)

    user_links = relationship("GameUser", back_populates="game", cascade="all, delete-orphan")
    platform_links = relationship("GamePlatform", back_populates="game", cascade="all, delete-orphan")
    publisher = relationship("Publisher", back_populates="games", uselist=False)
    genre = relationship("Genre", back_populates="games", uselist=False)
    sale = relationship("Sale", back_populates="game", uselist=False)

    linked_users = relationship("User", secondary="games_users", viewonly=True)
    linked_platforms = relationship("Platform", secondary="games_platforms", viewonly=True)


class GamePlatform(Base):
    """
    Table associative représentant la relation many-to-many entre jeux et plateformes.

    Attributs:
        game_id (Integer): Clé étrangère vers Game.id.
        platform_id (Integer): Clé étrangère vers Platform.id.
        release_year (Integer): Année de sortie du jeu sur la plateforme.
        game (relationship): Relation vers le jeu.
        platform (relationship): Relation vers la plateforme.
    """

    __tablename__ = "games_platforms"

    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), primary_key=True)
    release_year = Column(SmallInteger)

    game = relationship("Game", back_populates="platform_links")
    platform = relationship("Platform", back_populates="game_links")


class Platform(Base):
    """
    Modèle représentant une plateforme de jeu (ex: PC, PS5, Xbox).

    Attributs:
        id (Integer): Identifiant unique de la plateforme.
        name (String): Nom unique de la plateforme.
        game_links (relationship): Relations GamePlatform associant la plateforme aux jeux.
        linked_games (relationship): Jeux liés à la plateforme (lecture seule).
    """

    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    game_links = relationship("GamePlatform", back_populates="platform", cascade="all, delete-orphan")
    linked_games = relationship("Game", secondary="games_platforms", viewonly=True)


class Publisher(Base):
    """
    Modèle représentant un éditeur de jeux vidéo.

    Attributs:
        id (Integer): Identifiant unique de l'éditeur.
        name (String): Nom unique de l'éditeur.
        games (relationship): Jeux publiés par l'éditeur.
    """

    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    games = relationship("Game", back_populates="publisher", cascade="all, delete-orphan")


class Genre(Base):
    """
    Modèle représentant un genre de jeu vidéo (ex: RPG, FPS).

    Attributs:
        id (Integer): Identifiant unique du genre.
        name (String): Nom unique du genre.
        games (relationship): Jeux appartenant à ce genre.
    """

    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    games = relationship("Game", back_populates="genre", cascade="all, delete-orphan")


class Sale(Base):
    """
    Modèle représentant les ventes d'un jeu vidéo par région.

    Attributs:
        id (Integer): Identifiant unique de la vente.
        north_america (Float): Ventes en Amérique du Nord.
        europe (Float): Ventes en Europe.
        japan (Float): Ventes au Japon.
        other (Float): Ventes dans le reste du monde.
        total (Float): Ventes totales.
        game_id (Integer): Clé étrangère vers Game.id (unique).
        game (relationship): Relation vers le jeu correspondant.
    """

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    north_america = Column(Float(4,2), nullable=False)
    europe = Column(Float(4,2), nullable=False)
    japan = Column(Float(4,2), nullable=False)
    other = Column(Float(4,2), nullable=False)
    total = Column(Float(4,2), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, unique=True)

    game = relationship("Game", back_populates="sale", uselist=False)
