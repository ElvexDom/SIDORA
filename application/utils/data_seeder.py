from application.models.entities import *
from application.utils.crypto_tools import CryptoTools
from application.utils.log_watcher import LogWatcher
from random import sample, randint
from faker import Faker
import pandas as pd


class DataSeeder:
    """
    Classe utilitaire pour insérer et générer des données dans la base.

    Fournit des méthodes pour :
    - Générer des utilisateurs fictifs avec des jeux associés.
    - Lire des jeux depuis un CSV ou une liste de dictionnaires et les insérer en base.

    Attributs
    ---------
    session : SQLAlchemy Session
        Session utilisée pour les opérations en base.
    fake : Faker
        Instance Faker pour générer des données aléatoires.
    """

    session: object
    fake: Faker

    def __init__(self, session) -> None:
        """
        Initialise le DataSeeder avec une session SQLAlchemy.

        Paramètres
        ----------
        session : SQLAlchemy Session
            Session pour interagir avec la base de données.
        """
        self.session = session
        self.fake = Faker()

    def generate_fake_users_with_games(
        self, num_users: int = 50, min_games: int = 10, max_games: int = 20
    ) -> list[object]:
        """
        Génère des utilisateurs fictifs et leur assigne des jeux aléatoires.

        Paramètres
        ----------
        num_users : int, optionnel
            Nombre maximum d'utilisateurs à générer (par défaut 50).
        min_games : int, optionnel
            Nombre minimum de jeux par utilisateur (par défaut 10).
        max_games : int, optionnel
            Nombre maximum de jeux par utilisateur (par défaut 20).

        Retour
        ------
        list[User]
            Liste des utilisateurs générés.

        Effets secondaires
        -----------------
        Les utilisateurs et leurs relations avec les jeux sont ajoutés et commités en base.
        """
        users = []
        game_users_links = []

        try:
            all_games = self.session.query(Game).all()
            if not all_games:
                LogWatcher.log("warning", "Aucun jeu en base pour attribuer aux utilisateurs.", True)
                return []

            for _ in range(num_users):
                consent = self.fake.boolean(chance_of_getting_true=80)
                if not consent:
                    continue

                user = User(
                    pseudo=self.fake.unique.user_name(),
                    password=CryptoTools.hash_password(self.fake.password(length=10)),
                    mail=CryptoTools.hash_email(self.fake.unique.email()),
                    consent=True,
                    expiry=self.fake.date_between(start_date="today", end_date="+5y")
                )

                self.session.add(user)
                self.session.flush()  # récupère l'ID du user

                n_games = randint(min_games, min(max_games, len(all_games)))
                selected_games = sample(all_games, n_games)

                for game in selected_games:
                    existing_link = self.session.query(GameUser).filter_by(user_id=user.id, game_id=game.id).first()
                    if existing_link:
                        continue

                    link = GameUser(user=user, game=game)
                    self.session.add(link)
                    game_users_links.append(link)

                users.append(user)

            self.session.commit()
            LogWatcher.log("info", f"{len(users)} utilisateurs générés avec {len(game_users_links)} associations jeux.")
            return users

        except Exception as e:
            self.session.rollback()
            LogWatcher.log("error", f"Erreur lors de la génération de fake users : {e}", True)
            return []

    def read_and_insert_games(self, input_data) -> None:
        """
        Lit des jeux depuis un CSV ou une liste de dictionnaires et les insère en base.

        Paramètres
        ----------
        input_data : str | list[dict]
            Chemin vers un fichier CSV ou liste de dictionnaires représentant les jeux.

        Effets secondaires
        -----------------
        - Crée les objets Genre, Publisher et Platform si nécessaire.
        - Ajoute les jeux, les associations plateformes et les ventes en base.
        - Commit les changements.

        Exceptions
        ----------
        ValueError
            Si l'entrée n'est ni un CSV ni une liste de dictionnaires.
        Exception
            Toute autre erreur est loggée et relancée.
        """
        try:
            # Convertir input en DataFrame
            if isinstance(input_data, str):
                df = pd.read_csv(input_data)
            elif isinstance(input_data, list):
                df = pd.DataFrame(input_data)
            else:
                raise ValueError("Entrée invalide : fournir un chemin CSV ou une liste de dictionnaires.")

            # Synchronisation tables de référence
            all_genres = {g.name: g for g in self.session.query(Genre).all()}
            new_genres = [Genre(name=name) for name in df["Genre"].dropna().unique() if name not in all_genres]
            if new_genres:
                self.session.add_all(new_genres)
                self.session.flush()
                all_genres.update({g.name: g for g in new_genres})

            all_publishers = {p.name: p for p in self.session.query(Publisher).all()}
            new_publishers = [Publisher(name=name) for name in df["Publisher"].dropna().unique() if name not in all_publishers]
            if new_publishers:
                self.session.add_all(new_publishers)
                self.session.flush()
                all_publishers.update({p.name: p for p in new_publishers})

            all_platforms = {pl.name: pl for pl in self.session.query(Platform).all()}
            new_platforms = [Platform(name=name) for name in df["Platform"].dropna().unique() if name not in all_platforms]
            if new_platforms:
                self.session.add_all(new_platforms)
                self.session.flush()
                all_platforms.update({pl.name: pl for pl in new_platforms})

            # Création des objets
            games, game_platforms, sales = [], [], []

            for _, row in df.iterrows():
                genre_instance = all_genres.get(row.Genre, all_genres.get("Unknown"))
                publisher_instance = all_publishers.get(row.Publisher, all_publishers.get("Unknown"))
                platform_instance = all_platforms.get(row.Platform)

                game = Game(name=row.Name, rank=int(row.Rank), genre=genre_instance, publisher=publisher_instance)
                games.append(game)

                if platform_instance:
                    release_year = int(row.Year) if pd.notna(row.Year) else None
                    game_platform = GamePlatform(game=game, platform=platform_instance, release_year=release_year)
                    game_platforms.append(game_platform)

                sale = Sale(
                    game=game,
                    north_america=float(row.NA_Sales) if pd.notna(row.NA_Sales) else 0,
                    europe=float(row.EU_Sales) if pd.notna(row.EU_Sales) else 0,
                    japan=float(row.JP_Sales) if pd.notna(row.JP_Sales) else 0,
                    other=float(row.Other_Sales) if pd.notna(row.Other_Sales) else 0,
                    total=float(row.Global_Sales) if pd.notna(row.Global_Sales) else 0
                )
                sales.append(sale)

            # Ajouter tout et commit
            self.session.add_all(games)
            self.session.add_all(game_platforms)
            self.session.add_all(sales)
            self.session.commit()
            LogWatcher.log("info", f"{len(games)} jeux insérés avec succès.")

        except Exception as e:
            self.session.rollback()
            LogWatcher.log("error", f"Erreur lors de l'insertion des jeux : {e}")
            raise
