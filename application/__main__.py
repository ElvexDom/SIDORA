from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from application.models.entities import User, Game, UserGame, Platform, GamePlatform
from application.db.database import Session, engine

def executer_transaction():
    session = Session()
    try:
        # Création des utilisateurs
        users_neo = User(
            pseudo="Neo",
            password="matrix123",
            mail="neo@matrix.com",
            consent=True,
            limit_date=date(2026, 1, 1)
        )

        users_trinity = User(
            pseudo="Trinity",
            password="trinity123",
            mail="trinity@matrix.com",
            consent=True,
            limit_date=date(2026, 1, 1)
        )

        # Création des jeux
        game1 = Game(name="Cyber Battle", rank=1)
        game2 = Game(name="Matrix Reloaded", rank=2)

        # Création des liens UserGame
        link1 = UserGame(user=users_neo, game=game1)
        link2 = UserGame(user=users_neo, game=game2)

        # Création des platforms
        platform1 = Platform(name="Nintendo")
        platform2 = Platform(name="Activision")

        # Création des liens UserGame
        linkplatform1 = GamePlatform(game=game1, platform=platform1)
        linkplatform2 = GamePlatform(game=game2, platform=platform2)

        # Ajout à la session
        session.add_all([users_neo, users_trinity, game1, game2, link1, link2, platform1, platform2, linkplatform1, linkplatform2])

        # Commit
        session.commit()

        # Lecture des jeux de Neo via la relation user_games
        neo_games = [ug.game for ug in users_neo.user_games]

        print(f"Jeux de {users_neo.pseudo} :")
        for game in neo_games:
            print(f"  - ID: {game.id}, Name: {game.name}, Rank: {game.rank}")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Erreur transaction: {e}")

    finally:
        session.close()


if __name__ == "__main__":
    executer_transaction()
    engine.dispose()
