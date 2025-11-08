import requests
from app.core.config import settings

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY

def get_supabase_token(email: str, password: str) -> str:
    """Autentica no Supabase e retorna o access_token"""
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {"apikey": SUPABASE_KEY, "Content-Type": "application/json"}
    data = {"email": email, "password": password}

    response = requests.post(url, json=data)
    assert response.status_code == 200, f"❌ Supabase login failed: {response.text}"
    return response.json()["access_token"]
