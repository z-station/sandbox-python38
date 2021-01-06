from typing import TypedDict, List


class ResponseDebugDict(TypedDict):

    translator_output: str
    translator_error: str


class ResponseTestData(TypedDict):

    console_input: str
    console_output: str
    translator_console_output: str
    translator_console_error: str
    success: bool


class ResponseTestingDict(TypedDict):

    num: int
    num_success: int
    success: bool
    tests_data: List[ResponseTestData]
