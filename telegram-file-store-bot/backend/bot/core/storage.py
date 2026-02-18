import os
import uuid
import shutil
from core.config import STORAGE_PATH


class Storage:

    def __init__(self):
        os.makedirs(STORAGE_PATH, exist_ok=True)

    async def save(self, file_path: str):

        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file_path)[1]

        new_filename = f"{file_id}{ext}"
        new_path = os.path.join(STORAGE_PATH, new_filename)

        shutil.move(file_path, new_path)

        return file_id, new_path
