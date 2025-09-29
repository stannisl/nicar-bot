# bot.py
import discord
from discord.ext import commands
from config import settings
from utils.logger import logger
from handlers.commands import verify_command, help_command, cancel_command
from web.server import start_web_server
from shared import set_bot_instance  # Добавляем импорт
from handlers.oauth import oauth_handler  # Добавляем импорт

class SteamBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # Устанавливаем глобальную ссылку на бота ПЕРЕД запуском веб-сервера
        set_bot_instance(self)
        
        self.tree.add_command(verify_command)
        self.tree.add_command(help_command)
        self.tree.add_command(cancel_command)
        
        try:
            if settings.GUILD_ID:
                guild = discord.Object(id=settings.GUILD_ID)
                await self.tree.sync(guild=guild)
                logger.info(f"Commands synced for guild {settings.GUILD_ID}")
            else:
                await self.tree.sync()
                logger.info("Commands synced globally")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")

        # Запускаем веб-сервер
        
        try:
            self.web_runner = await start_web_server()
            logger.info("Web server started successfully")
        except Exception as e:
            logger.error(f"Failed to start web server: {e}")

    async def on_ready(self):
        logger.info(f'Bot is ready! Logged in as {self.user} (ID: {self.user.id})')
        logger.info(f'Verification link URL: {oauth_handler.get_oauth_url()}')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за верификациями"))

    async def close(self):
        """Очистка при завершении"""
        if hasattr(self, 'web_runner'):
            await self.web_runner.cleanup()
        await super().close()

bot = SteamBot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: Exception):
    logger.error(f"Command error: {error}")
    if interaction.response.is_done():
        await interaction.followup.send("❌ Произошла ошибка при выполнении команды", ephemeral=True)
    else:
        await interaction.response.send_message("❌ Произошла ошибка при выполнении команды", ephemeral=True)

def main():
    logger.info("Starting Discord bot...")
    try:
        bot.run(settings.DISCORD_BOT_TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()