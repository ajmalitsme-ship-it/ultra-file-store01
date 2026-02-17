import random, string, time
from pymongo import MongoClient
from config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)
db = client[DB_NAME]


def _code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


async def save_file(file_id):
    code = _code()
    db.files.insert_one({"code": code, "file_id": file_id})
    return code


def get_file(code):
    x = db.files.find_one({"code": code})
    return x["file_id"] if x else None


def add_user(user_id):
    if not db.users.find_one({"_id": user_id}):
        db.users.insert_one({"_id": user_id})


def get_all_users():
    return db.users.find({})


# premium
def add_premium(user_id, days):
    expire = int(time.time()) + days * 86400
    db.premium.update_one({"_id": user_id}, {"$set": {"expire": expire}}, upsert=True)


def is_premium(user_id):
    x = db.premium.find_one({"_id": user_id})
    return x and x["expire"] > int(time.time())
