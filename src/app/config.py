import os
from os import environ
from tempfile import gettempdir


TIMEOUT = 5  # seconds
SANDBOX_USER_UID = int(environ.get('SANDBOX_USER_UID', os.getuid()))
SANDBOX_DIR = environ.get('SANDBOX_DIR', gettempdir())
