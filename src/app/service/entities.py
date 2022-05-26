import os
import uuid
from collections import namedtuple
from app import config

ExecuteResult = namedtuple('ExecuteResult', ('result', 'error'))


class PythonFile:

    def __init__(self, code: str):
        self.filepath = os.path.join(config.SANDBOX_DIR, f'{uuid.uuid4()}.py')
        with open(self.filepath, 'w') as file:
            file.write(code)

    def remove(self):
        os.remove(self.filepath)
