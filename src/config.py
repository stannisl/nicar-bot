from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DISCORD_BOT_TOKEN: str
    VERIFY_URL: str
    DEBUG: bool = False
    RESULTS_FILE: str = "data.json"
    GUILD_ID: int = None
    MIN_DELAY_VERIFICATION: int = 5
    MAX_DELAY_VERIFICATION: int = 10

    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str
    OAUTH_SERVER_HOST: str = "localhost"
    OAUTH_SERVER_PORT: int = 8080
    START_WEB_SERVER: bool = False

    class Config:
        env_file = ".env"

settings = Settings()