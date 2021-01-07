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


class TestsFiles:

    def __init__(self, code: str):
        self._uuid = uuid.uuid4()
        self.filename_py = f'{self._uuid}.py'
        self.path_py = os.path.join(TMP_DIR, self.filename_py)
        self.paths_in = []

        with open(self.path_py, 'w') as file_py:
            file_py.write(code)

    def create_file_in(self, console_input: str):
        filename = f'{self._uuid}-{len(self.paths_in)}.in'
        path = os.path.join(TMP_DIR, filename)
        with open(path, 'w') as file:
            file.write(console_input)
        self.paths_in.append(path)
        return filename

    def remove(self):
        os.remove(self.path_py)
        while self.paths_in:
            os.remove(self.paths_in.pop())
