from application.utils.log_watcher import LogWatcher
import bcrypt
import hashlib


class CryptoTools:
    """
    Classe utilitaire pour les opérations de cryptographie.

    Fournit des méthodes pour :
    - Hasher et vérifier les mots de passe avec bcrypt.
    - Anonymiser et vérifier des emails avec SHA-256.

    Toutes les méthodes statiques loggent les erreurs via LogWatcher en cas d'échec.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash sécurisé d'un mot de passe en clair avec bcrypt.

        Paramètres
        ----------
        password : str
            Mot de passe en clair.

        Retour
        ------
        str
            Mot de passe hashé en UTF-8.

        Exceptions
        ----------
        RuntimeError
            Levée si le hashage échoue.
        """
        try:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            return hashed.decode("utf-8")
        except Exception as e:
            LogWatcher.log("error", f"Erreur lors du hashage du mot de passe : {e}")
            raise RuntimeError("Impossible de hasher le mot de passe") from e

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Vérifie qu'un mot de passe en clair correspond à un hash bcrypt stocké.

        Paramètres
        ----------
        password : str
            Mot de passe en clair à vérifier.
        hashed_password : str
            Mot de passe hashé stocké en base.

        Retour
        ------
        bool
            True si le mot de passe correspond, False sinon.

        Exceptions
        ----------
        RuntimeError
            Levée si la vérification échoue.
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hashed_password.encode("utf-8")
            )
        except Exception as e:
            LogWatcher.log("error", f"Erreur lors de la vérification du mot de passe : {e}")
            raise RuntimeError("Impossible de vérifier le mot de passe") from e

    @staticmethod
    def hash_email(email: str) -> str:
        """
        Hash SHA-256 pour anonymiser une adresse email.

        Non réversible, utilisable pour vérifier l'unicité ou comparer des emails
        sans stocker l'email en clair.

        Paramètres
        ----------
        email : str
            Adresse email en clair.

        Retour
        ------
        str
            Hash SHA-256 de l'email normalisé (minuscules, sans espaces).

        Exceptions
        ----------
        RuntimeError
            Levée si le hashage échoue.
        """
        try:
            normalized = email.strip().lower()
            return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        except Exception as e:
            LogWatcher.log("error", f"Erreur lors du hashage de l'email : {e}")
            raise RuntimeError("Impossible de hasher l'email") from e

    @staticmethod
    def verify_email(email: str, hashed_email: str) -> bool:
        """
        Vérifie qu'un email en clair correspond à un hash SHA-256 stocké.

        Paramètres
        ----------
        email : str
            Email en clair à vérifier.
        hashed_email : str
            Hash SHA-256 stocké.

        Retour
        ------
        bool
            True si le hash correspond à l'email, False sinon.

        Exceptions
        ----------
        RuntimeError
            Levée si la vérification échoue.
        """
        try:
            return CryptoTools.hash_email(email) == hashed_email
        except Exception as e:
            LogWatcher.log("error", f"Erreur lors de la vérification de l'email : {e}")
            raise RuntimeError("Impossible de vérifier l'email") from e
