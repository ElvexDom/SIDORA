from loguru import logger
from pathlib import Path
import sys


class LogWatcher:
    """
    Classe utilitaire pour la gestion centralisée des logs via Loguru.

    Cette classe configure automatiquement plusieurs fichiers de logs à l'import :
        - errors.log : niveau ERROR
        - warnings.log : niveau WARNING
        - info.log : niveau INFO
        - all.log : niveau DEBUG (tous les messages)

    Le dossier `logs/` est créé automatiquement s'il n'existe pas.
    Le handler par défaut de Loguru est supprimé pour éviter les doublons.

    Attributs de classe :
        LOG_DIR (Path) : Chemin vers le dossier contenant les fichiers de logs.

    Méthodes :
        log(level: str, message: str, screen: bool = False) -> None :
            Enregistre un message dans le fichier de log correspondant au niveau fourni.
            Si `screen=True`, affiche également le message sur la console avec format colorisé.

    Gestion des erreurs :
        Si un niveau de log inconnu est fourni, le message est enregistré en ERROR
        et affiché à l'écran si screen=True.
    """

    LOG_DIR: Path = Path("logs")

    # Création automatique du dossier à l'import
    LOG_DIR.mkdir(exist_ok=True)

    # Supprime le handler par défaut de Loguru
    logger.remove()

    # Fichiers de logs
    logger.add(
        LOG_DIR / "errors.log",
        level="ERROR",
        format="{time} {level} {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

    logger.add(
        LOG_DIR / "warnings.log",
        level="WARNING",
        format="{time} {level} {message}",
        rotation="10 MB"
    )

    logger.add(
        LOG_DIR / "info.log",
        level="INFO",
        format="{time} {level} {message}",
        rotation="10 MB"
    )

    logger.add(
        LOG_DIR / "all.log",
        level="DEBUG",
        format="{time} {level} {message}",
        rotation="20 MB"
    )

    @staticmethod
    def log(level: str, message: str, screen: bool = False) -> None:
        """
        Enregistre un message de log dans le fichier approprié et, optionnellement, sur la console.

        Parameters
        ----------
        level : str
            Niveau du log (ex : "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
        message : str
            Message à enregistrer.
        screen : bool, optional
            Si True, affiche également le message sur la console avec format colorisé. Par défaut False.

        Raises
        ------
        None
            Les erreurs internes sont capturées et loggées comme ERROR si le niveau est inconnu.
        """
        try:
            if screen:
                # Handler console temporaire
                handler_id = logger.add(
                    sys.stderr,
                    level="DEBUG",
                    colorize=True,
                    format=(
                        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
                        "<level>{level: ^8}</level> | "
                        "<cyan>{message}</cyan>"
                    )
                )
                logger.log(level.upper(), message)
                logger.remove(handler_id)  # Supprime uniquement ce handler
            else:
                logger.log(level.upper(), message)
        except ValueError:
            # Niveau de log inconnu
            msg: str = f"[NIVEAU INCONNU: {level}] {message}"
            logger.error(msg)
            if screen:
                print(msg)
