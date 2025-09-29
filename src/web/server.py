
from aiohttp import web
import discord
from handlers.oauth import oauth_handler
from utils.logger import logger
from shared import get_bot_instance, settings

class WebServer:
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        logger.info("WebServer initialized")

    def setup_routes(self):
        # Health check для мониторинга
        self.app.router.add_get('/health', self.health_check)
        # OAuth callback endpoint
        self.app.router.add_get('/oauth/callback', self.oauth_callback)

        logger.info("Web routes configured: /health, /oauth/callback")

    async def health_check(self, request):
        """Health check для мониторинга"""
        return web.Response(text="OK")

    async def redirect_to_oauth(self, request):
        """Редирект на OAuth URL"""
        oauth_url = oauth_handler.get_oauth_url()
        raise web.HTTPFound(oauth_url)

    async def oauth_callback(self, request):
        """Обработка OAuth2 callback - только логика отправки DM"""
        logger.info(f"OAuth callback received: {request.query}")
        
        code = request.query.get('code')
        error = request.query.get('error')
        
        if error:
            logger.error(f"OAuth error: {error}")
            return web.Response(text=f"Error: {error}", status=400)
        
        if not code:
            logger.error("No code provided in callback")
            return web.Response(text="Error: No authorization code", status=400)

        try:
            # Обмен code на access token
            token_data = await oauth_handler.exchange_code(code)
            if not token_data:
                return web.Response(text="Error: Token exchange failed", status=400)

            # Получение информации о пользователе
            user_info = await oauth_handler.get_user_info(token_data['access_token'])
            if not user_info:
                return web.Response(text="Error: Failed to get user info", status=400)

            user_id = int(user_info['id'])
            username = user_info['username']
            discriminator = user_info.get('discriminator', '0000')
            
            logger.info(f"OAuth success for user {username}#{discriminator} (ID: {user_id})")

            # Запуск DM диалога с пользователем
            success = await self.start_dm_verification(user_id, username, discriminator)
            
            if success:
                return web.Response(text="Verification started. Check your DMs.")
            else:
                return web.Response(text="Verification started but couldn't send DM. Please check if DMs are open.", status=400)
                
        except Exception as e:
            logger.error(f"Unexpected error in OAuth callback: {e}")
            return web.Response(text="Internal server error", status=500)

    async def start_dm_verification(self, user_id: int, username: str, discriminator: str) -> bool:
        """Запуск процесса верификации в ЛС, возвращает успешность"""
        try:
            bot = get_bot_instance()
            if not bot:
                logger.error("Bot instance not available")
                return False
                
            user = await bot.fetch_user(user_id)
            if not user:
                logger.error(f"Could not fetch user {user_id}")
                return False

            from handlers.views import create_language_view
            from locales.locales import get_localized_text
            from handlers.sessions import user_sessions
            
            # Проверяем активную сессию
            if user_id in user_sessions:
                logger.warning(f"User {user_id} already has active session")
                return True  # Уже есть сессия, считаем успехом
            
            # Отправляем приветственное сообщение
            embed = discord.Embed(
                title=get_localized_text("RU", "welcome"),
                description=get_localized_text("RU", "greeting"),
                color=0x0099ff
            )
            
            view = create_language_view()
            await user.send(embed=embed, view=view)
            logger.info(f"Started DM verification for user {username}#{discriminator}")
            return True
            
        except discord.Forbidden:
            logger.error(f"Could not DM user {username}#{discriminator} - DMs closed")
            return False
        except Exception as e:
            logger.error(f"Error starting DM verification: {e}")
            return False

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