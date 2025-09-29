# bot.py
import discord
from discord import app_commands
from discord.ext import commands
from config import settings
from utils.logger import logger
from handlers.commands import verify_command, help_command, cancel_command, ls_command
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
        set_bot_instance(self)
        
        self.tree.add_command(verify_command)
        self.tree.add_command(help_command)
        self.tree.add_command(ls_command)
        self.tree.add_command(cancel_command)

        try:
            if settings.GUILD_ID:
                guild = discord.Object(id=settings.GUILD_ID)
                synced = await self.tree.sync(guild=guild)
                logger.info(f"Commands synced for guild {settings.GUILD_ID}, synced: {len(synced)} commands")
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
    logger.error(f"Error type: {type(error)}")
    
    # Обработка отсутствия прав
    if isinstance(error, app_commands.MissingPermissions):
        missing_perms = error.missing_permissions
        missing_perms_text = ", ".join(missing_perms).replace("_", " ").title()
        
        embed = discord.Embed(
            title="❌ Недостаточно прав",
            description=f"Для выполнения этой команды требуются права: **{missing_perms_text}**",
            color=0xff0000
        )
        
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Обработка других типов ошибок прав
    elif isinstance(error, app_commands.BotMissingPermissions):
        missing_perms = error.missing_permissions
        missing_perms_text = ", ".join(missing_perms).replace("_", " ").title()
        
        embed = discord.Embed(
            title="❌ У бота недостаточно прав",
            description=f"Боту требуются права: **{missing_perms_text}**",
            color=0xff0000
        )
        
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Обработка ошибки "команда не найдена"
    elif isinstance(error, app_commands.CommandNotFound):
        logger.error("Command not found - sync issue?")
        embed = discord.Embed(
            title="❌ Команда не найдена",
            description="Эта команда временно недоступна. Попробуйте позже.",
            color=0xff0000
        )
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Обработка ошибки проверки (checks)
    elif isinstance(error, app_commands.CheckFailure):
        embed = discord.Embed(
            title="❌ Ошибка доступа",
            description="У вас нет прав для выполнения этой команды.",
            color=0xff0000
        )
        
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        return
        
    # Общая обработка остальных ошибок
    logger.error(f"Unhandled command error: {error}", exc_info=True)
    
    embed = discord.Embed(
        title="❌ Произошла ошибка",
        description="При выполнении команды произошла непредвиденная ошибка.",
        color=0xff0000
    )
    
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)

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