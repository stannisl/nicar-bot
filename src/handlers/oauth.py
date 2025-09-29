# handlers/oauth.py
import aiohttp
from typing import Dict, Optional
from config import settings
from utils.logger import logger

class OAuthHandler:
    def __init__(self):
        self.client_id = settings.DISCORD_CLIENT_ID
        self.client_secret = settings.DISCORD_CLIENT_SECRET
        self.redirect_uri = settings.DISCORD_REDIRECT_URI

    async def exchange_code(self, code: str) -> Optional[Dict]:
        """Обмен authorization code на access token"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://discord.com/api/oauth2/token', 
                                      data=data, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"OAuth token exchange failed: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"OAuth exchange error: {e}")
            return None

    async def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Получение информации о пользователе через access token"""
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://discord.com/api/users/@me', 
                                     headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"User info fetch failed: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"User info error: {e}")
            return None

    def get_oauth_url(self) -> str:
        """Генерация URL для OAuth2 авторизации"""
        scopes = ["identify", "guilds.join"]
        return (f"https://discord.com/oauth2/authorize"
                f"?client_id={self.client_id}"
                f"&redirect_uri={self.redirect_uri}"
                f"&response_type=code"
                f"&scope={'%20'.join(scopes)}")

oauth_handler = OAuthHandler()