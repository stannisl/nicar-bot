import logging
import sys
from loguru import logger

class LoguruHandler(logging.Handler):
    """Перехватчик для перенаправления logging в loguru"""
    
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
            
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_discord_logging():
    """Настройка логирования для discord.py"""
    
    discord_logger = logging.getLogger('discord')
    discord_logger.handlers = [LoguruHandler()]
    discord_logger.setLevel(logging.INFO)
    discord_logger.propagate = False
    
    logging.getLogger('discord.http').setLevel(logging.WARNING)
    logging.getLogger('discord.gateway').setLevel(logging.WARNING)
    logging.getLogger('discord.state').setLevel(logging.WARNING)