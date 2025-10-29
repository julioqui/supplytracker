from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.DB_URL = os.getenv("SUPABASE_DB_URL")
        self.TEST_DB_URL = os.getenv("TEST_DB_URL")

        # Choose DB based on environment
        if self.APP_ENV == "test":
            self.DB_URL = self.TEST_DB_URL
        else:
            self.DB_URL = self.DB_URL

        # --- JWT ---
        self.JWT_SECRET = os.getenv("JWT_SECRET")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

settings = Settings()
