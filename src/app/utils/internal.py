from typing import Tuple
from app.utils.msg import READ_ONLY_FS, TIMEOUT


def process_translator_error(stderr: bytes) -> str:

    """ Обработка текста сообщения об ошибке """

    result = clear_text(
        re.sub(pattern=r'\s*File.+.py",', repl="", string=stderr.decode())
    )
    if 'Terminated' in result:
        return TIMEOUT
    elif 'Read-only file system' in result:
        return READ_ONLY_FS
    else:
        return result


def process_translator_response(stdout: bytes, stderr: bytes) -> Tuple[str, str]:

    """ Преобразует bytes (вывод интерпретатора) в unicode, удаляет лишние символы из вывода """

    output = '' if stdout is None else stdout.decode()
    error = '' if stderr is None else process_translator_error(stderr)
    return output, error
