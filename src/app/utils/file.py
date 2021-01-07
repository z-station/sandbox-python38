import os
import uuid
from app.config import TMP_DIR


class PyFile:

    def __init__(self, code: str):
        self.filepath = os.path.join(TMP_DIR, f'{uuid.uuid4()}.py')
        with open(self.filepath, 'w') as file:
            file.write(code)

    def remove(self):
        os.remove(self.filepath)
