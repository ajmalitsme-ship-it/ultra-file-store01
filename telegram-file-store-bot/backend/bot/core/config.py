import os
from dotenv import load_dotenv

load_dotenv()


# =========================
# Telegram
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")

# =========================
# Owner / Admin
# =========================
OWNER_ID = int(os.getenv("OWNER_ID", 0))

# =========================
# Database
# =========================
MONGO_URI = os.getenv("MONGO_URI")

# =========================
# Web App
# =========================
WEB_APP_URL = os.getenv("WEB_APP_URL", "http://localhost:8000")

# =========================
# Storage
# =========================
STORAGE_PATH = os.getenv("STORAGE_PATH", "./files")

# =========================
# Limits
# =========================
FREE_FILE_LIMIT_MB = int(os.getenv("FREE_FILE_LIMIT_MB", 100))
PREMIUM_FILE_LIMIT_MB = int(os.getenv("PREMIUM_FILE_LIMIT_MB", 2048))

# =========================
# ForceSub
# =========================
FORCE_SUB_ENABLED = os.getenv("FORCE_SUB_ENABLED", "true").lower() == "true"

# =========================
# Redis (Rate Limit)
# =========================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
