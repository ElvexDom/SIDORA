import bcrypt
import hashlib


class CryptoTools:
    """
    Classe utilitaire pour les opérations de cryptographie :
    - Hash sécurisé des mots de passe
    - Anonymisation des emails
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash sécurisé du mot de passe avec bcrypt.

        :param password: Mot de passe en clair
        :return: Mot de passe hashé (string UTF-8)
        """
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Vérifie un mot de passe en clair contre un hash bcrypt.

        :param password: Mot de passe en clair
        :param hashed_password: Mot de passe hashé stocké
        :return: True si valide, False sinon
        """
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    @staticmethod
    def hash_email(email: str) -> str:
        """
        Anonymisation de l'email par SHA-256.
        Non réversible, utilisable pour vérification ou unicité.

        :param email: Adresse email en clair
        :return: Hash SHA-256 de l'email normalisé
        """
        normalized = email.strip().lower()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def verify_email(email: str, hashed_email: str) -> bool:
        """
        Vérifie un email en clair contre un hash SHA-256.

        :param email: Email en clair à vérifier
        :param hashed_email: Hash SHA-256 stocké
        :return: True si correspond, False sinon
        """
        return CryptoTools.hash_email(email) == hashed_email
