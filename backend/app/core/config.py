from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.DB_URL = os.getenv("SUPABASE_DB_URL")
        self.SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        self.SUPABASE_URL = os.getenv("SUPABASE_URL")
        self.SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
        self.TEST_DB_URL = os.getenv("TEST_DB_URL")
        self.CORS_ORIGINS = os.getenv("CORS_ORIGINS")
        self.CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS")
        self.CORS_METHODS = os.getenv("CORS_METHODS")
        self.CORS_HEADERS = os.getenv("CORS_HEADERS")

        # Choose DB based on environment
        if self.APP_ENV == "test":
            self.DB_URL = self.TEST_DB_URL
        else:
            self.DB_URL = self.DB_URL

settings = Settings()
