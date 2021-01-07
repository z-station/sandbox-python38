import subprocess
from flask import Flask, request
from app.entities.request import (
    RequestDebugDict,
    RequestTestData,
    RequestTestingDict
)
from app.entities.response import (
    ResponseDebugDict,
    ResponseTestData,
    ResponseTestingDict
)
from app.utils.files import (
    PyFile,
    TestsFiles
)
from app.utils.translator import (
    process_translator_response,
    clear
)
from app import config
from app.utils import msg

app = Flask(__name__)


@app.route('/debug', methods=['post'])
def debug() -> ResponseDebugDict:
    data: RequestDebugDict = request.json
    console_input: str = clear(data.get('console_input', ''))
    code: str = clear(data['code'])

    file = PyFile(code)

    try:
        proc = subprocess.Popen(
            args=['python', file.filepath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = proc.communicate(
            input=console_input.encode('utf-8'),
            timeout=config.TIMEOUT
        )
        proc.kill()
    except subprocess.TimeoutExpired:
        output, error = '', msg.TIMEOUT
    except Exception as e:
        output, error = '', f'Неожиданное исключение: {e}'
    else:
        output, error = process_translator_response(
            stdout=stdout,
            stderr=stderr
        )
    file.remove()
    return ResponseDebugDict(
        translator_output=output,
        translator_error=error
    )


@app.route('/testing', methods=['post'])
def testing() -> ResponseTestingDict:
    num = len(request['tests'])
    num_success = num
    success = num == num_success
    return ResponseTestingDict(
        num=num,
        num_success=num_success,
        success=success,
        tests_data=[
            ResponseTestData(
                console_input=test['console_input'],
                console_output=test['console_output'],
                translator_console_output='test_output',
                translator_console_error='test_error',
                success=True
            ) for test in request['tests']
        ]
    )

