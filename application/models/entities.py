from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    pseudo = Column(String, nullable=False)
    password = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    consent = Column(Boolean, nullable=False)
    expiry = Column(Date, nullable=False)

    user_game_links = relationship("UserGame", back_populates="user", cascade="all, delete-orphan")
    linked_games = relationship("Game", secondary="games_users", viewonly=True)

class UserGame(Base):
    __tablename__ = "games_users"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)

    user = relationship("User", back_populates="user_game_links")
    game = relationship("Game", back_populates="user_game_links")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(Integer, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

    game_user_links = relationship("UserGame", back_populates="game", cascade="all, delete-orphan")
    linked_users = relationship("User", secondary="games_users", viewonly=True)

    game_platform_links = relationship("GamePlatform", back_populates="game", cascade="all, delete-orphan")
    linked_platforms = relationship("Platform", secondary="games_has_platforms", viewonly=True)

    game_publisher_links = relationship("Publisher", back_populates="game", cascade="all, delete-orphan")
    game_genre_links = relationship("Genre", back_populates="game", cascade="all, delete-orphan")


class GamePlatform(Base):
    __tablename__ = "games_has_platforms"  # on garde le nom de table

    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    platform_id = Column(Integer, ForeignKey("platform.id"), primary_key=True)

    # back_populates doit correspondre aux noms dans Game et Platform
    GamePlatform = relationship("Game", back_populates="platform_links")
    platform = relationship("Platform", back_populates="platform_links")
    release_year = Column(Integer, nullable=False)

class Platform(Base):
    __tablename__ = "platform"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # relation vers GamePlatform
    platform_links = relationship("GamePlatform", back_populates="platform", cascade="all, delete-orphan")

    # accès rapide aux utilisateurs liés (lecture seule)
    game = relationship("Game", secondary="games_has_platforms", viewonly=True)
    
class Publisher(Base):
    __tablename__ = "pubishers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # relation vers GamePlatform
    game = relationship("Game", back_populates="game_publisher", cascade="all, delete-orphan")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # relation vers Game
    game_genre = relationship("Game", back_populates="game_genre", cascade="all, delete-orphan")



