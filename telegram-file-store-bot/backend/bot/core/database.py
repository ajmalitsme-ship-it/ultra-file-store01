from motor.motor_asyncio import AsyncIOMotorClient
from core.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["telegram_file_store"]

# Collections:
# db.users
# db.files
# db.batches
# db.admins
# db.force_sub
# db.premium
