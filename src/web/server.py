from aiohttp import web
import aiohttp_jinja2
import jinja2
from pathlib import Path
import discord
from handlers.oauth import oauth_handler
from utils.logger import logger
from shared import get_bot_instance, settings

class WebServer:
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        
        # Настройка шаблонов
        templates_path = Path(__file__).parent / 'templates'
        aiohttp_jinja2.setup(self.app, loader=jinja2.FileSystemLoader(templates_path))

    def setup_routes(self):
        self.app.router.add_get('/oauth/callback', self.oauth_callback)

        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/success', self.success)
        self.app.router.add_get('/error', self.error)

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        """Главная страница с кнопкой 'Add Discord'"""
        return {
            'oauth_url': oauth_handler.get_oauth_url(),
            'verify_url': settings.VERIFY_URL
        }

    async def oauth_callback(self, request):
        """Обработка OAuth2 callback"""
        code = request.query.get('code')
        error = request.query.get('error')
        
        if error:
            logger.error(f"OAuth error: {error}")
            return web.HTTPFound('/error')
        
        if not code:
            logger.error("No code provided in callback")
            return web.HTTPFound('/error')

        # Обмен code на access token
        token_data = await oauth_handler.exchange_code(code)
        if not token_data:
            return web.HTTPFound('/error')

        # Получение информации о пользователе
        user_info = await oauth_handler.get_user_info(token_data['access_token'])
        if not user_info:
            return web.HTTPFound('/error')

        user_id = int(user_info['id'])
        username = user_info['username']
        discriminator = user_info.get('discriminator', '0000')
        
        logger.info(f"OAuth success for user {username}#{discriminator} (ID: {user_id})")

        # Запуск DM диалога с пользователем
        await self.start_dm_verification(user_id, username, discriminator)
        
        return web.HTTPFound('/success')

    async def start_dm_verification(self, user_id: int, username: str, discriminator: str):
        """Запуск процесса верификации в ЛС"""
        try:
            bot = get_bot_instance()
            if not bot:
                logger.error("Bot instance not available")
                return
                
            user = await bot.fetch_user(user_id)
            if user:
                # Используем существующую логику из verify_command
                from handlers.views import create_language_view
                from locales.locales import get_localized_text
                from handlers.sessions import user_sessions
                
                # Проверяем активную сессию
                if user_id in user_sessions:
                    logger.warning(f"User {user_id} already has active session")
                    return
                
                # Отправляем приветственное сообщение
                embed = discord.Embed(
                    title=get_localized_text("RU", "welcome"),
                    description=get_localized_text("RU", "greeting"),
                    color=0x0099ff
                )
                
                view = create_language_view()
                await user.send(embed=embed, view=view)
                logger.info(f"Started DM verification for user {username}#{discriminator}")
                
        except discord.Forbidden:
            logger.error(f"Could not DM user {username}#{discriminator} - DMs closed")
        except Exception as e:
            logger.error(f"Error starting DM verification: {e}")

    @aiohttp_jinja2.template('success.html')
    async def success(self, request):
        return {}

    @aiohttp_jinja2.template('error.html')
    async def error(self, request):
        return {}

def create_web_server():
    return WebServer()

async def start_web_server():
    server = create_web_server()
    runner = web.AppRunner(server.app)
    await runner.setup()
    
    site = web.TCPSite(runner, settings.OAUTH_SERVER_HOST, settings.OAUTH_SERVER_PORT)
    await site.start()
    
    logger.info(f"Web server started on {settings.OAUTH_SERVER_HOST}:{settings.OAUTH_SERVER_PORT}")
    return runner