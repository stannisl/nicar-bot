from loguru import logger
import sys
from .discord_logger import setup_discord_logging

logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)
logger.add(
    "logs/bot.log",
    rotation="500 MB",
    retention="10 days",
    level="DEBUG"
)

setup_discord_logging()