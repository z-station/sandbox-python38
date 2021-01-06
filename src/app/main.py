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
app = Flask(__name__)


@app.route('/debug', methods=['post'])
def debug() -> ResponseDebugDict:
    output = 'test output'
    error = 'test error'
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

