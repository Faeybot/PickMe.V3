import os

TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot Token
DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL URL dari Railway

FEED_LIMIT_TEXT = 3
FEED_LIMIT_PHOTO = 1
SWIPE_LIMIT = 20

FEED_CHANNEL = os.getenv("FEED_CHANNEL")  # Channel feed ID (privat admin)
ADMIN_CHANNEL = os.getenv("ADMIN_CHANNEL")  # Channel admin untuk block/report
