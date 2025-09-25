from telegram.ext import Application
from config import settings
from handlers.commands import get_conversation_handler, help_command
from utils.logger import logger
from telegram.ext import CommandHandler

def main():
    application = (
        Application.builder()
        .token(settings.BOT_TOKEN)
        .build()
    )

    conv = get_conversation_handler()
    application.add_handler(conv)

    application.add_handler(CommandHandler("help", help_command))

    logger.info("Starting bot...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
