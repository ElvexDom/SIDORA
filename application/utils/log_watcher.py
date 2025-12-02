from loguru import logger
from pathlib import Path
import sys

class LogWatcher:
    LOG_DIR = Path("logs")

    # Setup automatique à l'import
    LOG_DIR.mkdir(exist_ok=True)

    # Supprime le handler par défaut de Loguru
    logger.remove()

    # Fichiers logs
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
    def log(level: str, message: str, screen: bool = False):
        """
        Log dans les fichiers, et éventuellement sur la console si screen=True.
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
            msg = f"[NIVEAU INCONNU: {level}] {message}"
            logger.error(msg)
            if screen:
                print(msg)
