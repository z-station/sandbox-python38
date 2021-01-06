from typing import TypedDict, List


class CheckersDict(TypedDict):

    console_output: str


class RequestDebugDict(TypedDict):

    console_input: str
    code: str


class RequestTestData(TypedDict):

    console_input: str
    console_output: str


class RequestTestingDict(TypedDict):

    checkers: CheckersDict
    tests: List[RequestTestData]
    code: str
