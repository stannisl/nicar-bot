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

    class Config:
        env_file = ".env"

settings = Settings()