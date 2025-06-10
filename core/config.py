from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
WEBHOOK_DOMAIN = os.getenv('WEBHOOK_DOMAIN', '')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', '/webhook')
WEBHOOK_URL = WEBHOOK_DOMAIN + WEBHOOK_PATH

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite://db.sqlite3')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')
