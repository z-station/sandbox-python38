import pytest
from unittest.mock import call
from app.service.main import PythonService
from app import config
from app.entities import (
    DebugData,
    TestsData,
    TestData
)
from app.service.entities import ExecuteResult
from app.service.entities import PythonFile
from app.service.exceptions import CheckerException
from app.service import messages
from app.service import exceptions


def test_execute__float_result__ok():

    """ Задача "Дробная часть" """

    # arrange
    code = 'print(17.9%1)'
    file = PythonFile(code)

    # act
    exec_result = PythonService._execute(file=file)

    # assert
    assert round(float(exec_result.result), 1) == 0.9
    assert exec_result.error is None
    file.remove()


def test_execute__data_in_is_integer__ok():

    """ Задача "Делёж яблок" """

    # arrange
    data_in = (
        '6\n'
        '50'
    )
    code = (
       'n = int(input())\n'
       'k = int(input())\n'
       'print(k//n)\n'
       'print(k%n)'
    )
    file = PythonFile(code)

    # act
    exec_result = PythonService._execute(file=file, data_in=data_in)

    # assert
    assert exec_result.result == (
        '8\n'
        '2'
    )
    assert exec_result.error is None
    file.remove()


def test_execute__data_in_is_string__ok():

    # arrange
    data_in = 'Abrakadabra'
    code = (
        's = input()\n'
        'print(s[::-2])'
    )
    file = PythonFile(code)

    # act
    exec_result = PythonService._execute(
        data_in=data_in,
        file=file
    )

    # assert
    assert exec_result.result == 'abdkrA'
    assert exec_result.error is None
    file.remove()


def test_execute__empty_result__return_none():

    # arrange
    code = 'test = 1'
    file = PythonFile(code)

    # act
    exec_result = PythonService._execute(
        file=file
    )

    # assert
    assert exec_result.result is None
    assert exec_result.error is None
    file.remove()


def test_execute__timeout__raise_exception(mocker):

    # arrange
    code = (
        'while True:\n'
        '  pass'
    )
    file = PythonFile(code)
    mocker.patch('app.config.TIMEOUT', 1)

    # act
    with pytest.raises(exceptions.TimeoutException) as ex:
        PythonService._execute(file=file)

    # assert
    assert ex.value.message == messages.MSG_1
    file.remove()


def test_execute__proc_exception__raise_exception(mocker):

    # arrange
    code = 'Some code'
    data_in = 'Some data in'
    file = PythonFile(code)
    communicate_mock = mocker.patch(
        'subprocess.Popen.communicate',
        side_effect=Exception()
    )

    # act
    with pytest.raises(exceptions.ExecutionException) as ex:
        PythonService._execute(file=file, data_in=data_in)

    # assert
    assert ex.value.message == messages.MSG_6
    communicate_mock.assert_called_once_with(
        input=data_in,
        timeout=config.TIMEOUT
    )
    file.remove()


def test_check__true__ok():

    # arrange
    value = 'some value'
    right_value = 'some value'
    checker_func = (
        'def checker(right_value: str, value: str) -> bool:'
        '  return right_value == value'
    )

    # act
    check_result = PythonService._check(
        checker_func=checker_func,
        right_value=right_value,
        value=value
    )

    # assert
    assert check_result is True


def test_check__false__ok():

    # arrange
    value = 'invalid value'
    right_value = 'some value'
    checker_func = (
        'def checker(right_value: str, value: str) -> bool:'
        '  return right_value == value'
    )

    # act
    check_result = PythonService._check(
        checker_func=checker_func,
        right_value=right_value,
        value=value
    )

    # assert
    assert check_result is False


def test_check__invalid_checker_func__raise_exception():

    # arrange
    checker_func = (
        'def my_checker(right_value: str, value: str) -> bool:'
        '  return right_value == value'
    )

    # act
    with pytest.raises(CheckerException) as ex:
        PythonService._check(
            checker_func=checker_func,
            right_value='value',
            value='value'
        )

    # assert
    assert ex.value.message == messages.MSG_2


def test_check__checker_func_no_return_instruction__raise_exception():

    # arrange
    checker_func = (
        'def checker(right_value: str, value: str) -> bool:'
        '  result = right_value == value'
    )

    # act
    with pytest.raises(CheckerException) as ex:
        PythonService._check(
            checker_func=checker_func,
            right_value='value',
            value='value'
        )

    # assert
    assert ex.value.message == messages.MSG_3


def test_check__checker_func_return_not_bool__raise_exception():

    # arrange
    checker_func = (
        'def checker(right_value: str, value: str) -> bool:'
        '  return None'
    )

    # act
    with pytest.raises(CheckerException) as ex:
        PythonService._check(
            checker_func=checker_func,
            right_value='value',
            value='value'
        )

    # assert
    assert ex.value.message == messages.MSG_4


def test_check__checker_func__invalid_syntax__raise_exception():

    # arrange
    checker_func = (
        'def checker(right_value: str, value: str) -> bool:'
        '  include(invalid syntax here)'
        '  return True'
    )

    # act
    with pytest.raises(CheckerException) as ex:
        PythonService._check(
            checker_func=checker_func,
            right_value='value',
            value='value'
        )

    # assert
    assert ex.value.message == messages.MSG_5
    assert ex.value.details == 'invalid syntax (<string>, line 1)'


def test_debug__ok(mocker):

    # arrange
    execute_result = ExecuteResult(
        result='some execute code result',
        error='some compilation error'
    )
    execute_mock = mocker.patch(
        'app.service.main.PythonService._execute',
        return_value=execute_result
    )
    file_mock = mocker.Mock()
    file_mock.remove = mocker.Mock()
    mocker.patch.object(PythonFile, '__new__', return_value=file_mock)
    data = DebugData(
        code='some code',
        data_in='some data_in'
    )

    # act
    debug_result = PythonService.debug(data)

    # assert
    assert debug_result.result == execute_result.result
    assert debug_result.error == execute_result.error
    file_mock.remove.assert_called_once()
    execute_mock.assert_called_once_with(
        file=file_mock,
        data_in=data.data_in
    )


def test_testing__ok(mocker):

    # arrange
    execute_result = ExecuteResult(
        result='some execute code result',
        error='some compilation error'
    )
    execute_mock = mocker.patch(
        'app.service.main.PythonService._execute',
        return_value=execute_result
    )
    file_mock = mocker.Mock()
    file_mock.remove = mocker.Mock()
    mocker.patch.object(PythonFile, '__new__', return_value=file_mock)
    check_result = mocker.Mock()
    check_mock = mocker.patch(
        'app.service.main.PythonService._check',
        return_value=check_result
    )
    test_1 = TestData(
        data_in='some test input 1',
        data_out='some test out 1'
    )
    test_2 = TestData(
        data_in='some test input 2',
        data_out='some test out 2'
    )

    data = TestsData(
        code='some code',
        checker='some checker',
        tests=[test_1, test_2]
    )

    # act
    testing_result = PythonService.testing(data)

    # assert
    tests_result = testing_result.tests
    assert len(tests_result) == 2
    assert tests_result[0].result == execute_result.result
    assert tests_result[0].error == execute_result.error
    assert tests_result[0].ok == check_result
    assert tests_result[1].result == execute_result.result
    assert tests_result[1].error == execute_result.error
    assert tests_result[1].ok == check_result
    assert execute_mock.call_args_list == [
        call(
            file=file_mock,
            data_in=test_1.data_in
        ),
        call(
            file=file_mock,
            data_in=test_2.data_in
        )
    ]
    assert check_mock.call_args_list == [
        call(
            checker_func=data.checker,
            right_value=test_1.data_out,
            value=execute_result.result
        ),
        call(
            checker_func=data.checker,
            right_value=test_2.data_out,
            value=execute_result.result
        )
    ]
    file_mock.remove.assert_called_once()
