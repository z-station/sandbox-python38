from typing import TypedDict, List


class RequestDebugDict(TypedDict):

    translator_console_input: str
    code: str


class RequestTestData(TypedDict):

    test_console_input: str
    test_console_output: str


class RequestTestingDict(TypedDict):

    checker_code: str
    tests_data: List[RequestTestData]
    code: str
