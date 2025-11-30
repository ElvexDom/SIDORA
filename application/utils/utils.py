from pathlib import Path
import hashlib
import bcrypt
from faker import Faker
import pandas as pd
from application.models.entities import *

fake = Faker()

def hash_password(password: str) -> str:
    """
    Hash sécurisé du mot de passe avec bcrypt.
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def hash_email(email: str) -> str:
    """
    Anonymisation de l'email par SHA-256.
    Non réversible, peut seulement être utilisé pour vérification/unicité.
    """
    normalized = email.strip().lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def generate_fake_users(num_users=50):
    """
    Génère des utilisateurs avec :
    - mot de passe hashé (bcrypt)
    - email anonymisé (SHA-256)
    
    Seuls les utilisateurs avec consentement sont stockés.
    Expiry définit la durée de conservation pour conformité RGPD.
    """
    users = []

    for _ in range(num_users):
        consent = fake.boolean(chance_of_getting_true=80)  # 80% de consentement simulé
        if not consent:
            continue  # Ne pas stocker les données si consentement False

        raw_password = fake.password(length=10)
        raw_mail = fake.unique.email()  # donnée sensible fictive

        user = User(
            pseudo=fake.unique.user_name(),
            password=hash_password(raw_password),
            mail=hash_email(raw_mail),
            consent=True,
            expiry=fake.date_between(start_date="today", end_date="+5y")
        )
        users.append(user)

    return users

def generate_fake_users_with_games(session, num_users=50, min_games=10, max_games=20):
    from random import sample, randint
    from application.models.entities import User, Game, GameUser
    
    all_games = session.query(Game).all()
    if not all_games:
        print("[WARN] Aucun jeu en base pour attribuer aux utilisateurs.")
        return []

    users = []

    for _ in range(num_users):
        consent = fake.boolean(chance_of_getting_true=80)
        if not consent:
            continue

        user = User(
            pseudo=fake.unique.user_name(),
            password=hash_password(fake.password(length=10)),
            mail=hash_email(fake.unique.email()),
            consent=True,
            expiry=fake.date_between(start_date="today", end_date="+5y")
        )

        n_games = randint(min_games, min(max_games, len(all_games)))
        selected_games = sample(all_games, n_games)

        # Crée les objets GameUser pour lier l'utilisateur aux jeux
        for game in selected_games:
            link = GameUser(user=user, game=game)
            user.game_links.append(link)  # ou session.add(link) directement

        session.add(user)
        users.append(user)

    session.commit()
    print(f"[INFO] {len(users)} utilisateurs insérés avec leurs jeux.")
    return users


def read_csv_to_df(input_data):
    """
    Convertit un fichier CSV ou une liste de dictionnaires en un DataFrame pandas.

    Args:
        input_data (str ou list):
            - str : chemin vers un fichier CSV unique
            - list : liste de dictionnaires représentant les lignes de données

    Returns:
        pd.DataFrame : DataFrame pandas correspondant aux données fournies

    Raises:
        ValueError : si l'entrée n'est ni un chemin CSV ni une liste de dictionnaires
    """

    # input_data est un chemin vers un fichier CSV
    if isinstance(input_data, str):
        return pd.read_csv(input_data)
    
    # input_data est une liste de dictionnaires
    if isinstance(input_data, list):
        return pd.DataFrame(input_data)
    
    # entrée invalide
    raise ValueError("Entrée invalide : fournir un chemin CSV ou une liste de dictionnaires.")


def sync_table_from_df(session, df: pd.DataFrame, model, column_name: str):
    # --- Valeurs uniques dans le DataFrame ---
    unique_values = df[column_name].dropna().unique().tolist()
    
    # --- Récupérer les éléments existants en base ---
    existing_items = {g.name: g for g in session.query(model).all()}

    # --- Créer les nouvelles entrées non présentes en base ---
    new_items = [model(name=v) for v in unique_values if v not in existing_items]
    if new_items:
        session.add_all(new_items)
        session.commit()
        for item in new_items:
            existing_items[item.name] = item

    return existing_items


def generate_and_insert_games(df: pd.DataFrame, session):
    # --- Synchroniser les tables de référence ---
    all_genres = sync_table_from_df(session, df, Genre, "Genre")
    all_publishers = sync_table_from_df(session, df, Publisher, "Publisher")
    all_platforms = sync_table_from_df(session, df, Platform, "Platform")

    games = []
    game_platforms = []
    sales = []

    for _, row in df.iterrows():
        genre_instance = all_genres.get(row.Genre, all_genres["Unknown"])
        publisher_instance = all_publishers.get(row.Publisher, all_publishers["Unknown"])
        platform_instance = all_platforms.get(row.Platform)

        game = Game(
            name=row.Name,
            rank=int(row.Rank),
            genre=genre_instance,
            publisher=publisher_instance
        )
        games.append(game)

        if platform_instance:
            release_year = int(row.Year) if pd.notna(row.Year) else None
            game_platform = GamePlatform(
                game=game,
                platform=platform_instance,
                release_year=release_year
            )
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

    # --- Ajouter **tout** dans la session avant le commit ---
    session.add_all(list(all_genres.values()))
    session.add_all(list(all_publishers.values()))
    session.add_all(list(all_platforms.values()))
    session.add_all(games)
    session.add_all(game_platforms)
    session.add_all(sales)
    session.commit()
    print(f"[INFO] Tout inséré avec succès : {len(games)} jeux, {len(game_platforms)} game-platforms, {len(sales)} ventes.")