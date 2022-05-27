import os
import subprocess
from typing import Optional
from app.service.entities import PythonFile
from app.entities import (
    DebugData,
    TestsData,

)
from app import config
from app.service import exceptions
from app.service.entities import ExecuteResult
from app.service import messages
from app.utils import clean_str, clean_error


class PythonService:

    @classmethod
    def _preexec_fn(cls):
        def change_process_user():
            os.setgid(config.SANDBOX_USER_UID)
            os.setuid(config.SANDBOX_USER_UID)
        return change_process_user()

    @classmethod
    def _execute(
        cls,
        file: PythonFile,
        data_in: Optional[str] = None
    ) -> ExecuteResult:

        """ Передает компилятору код программы и входные данные
            возвращает результат работы программы, либо ошибку компиляции """

        proc = subprocess.Popen(
            args=['python', file.filepath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=cls._preexec_fn,
            text=True
        )
        try:
            result, error = proc.communicate(
                input=data_in,
                timeout=config.TIMEOUT
            )
        except subprocess.TimeoutExpired:
            raise exceptions.TimeoutException()
        except Exception as ex:
            raise exceptions.ExecutionException(details=str(ex))
        else:
            return ExecuteResult(
                result=clean_str(result or None),
                error=clean_error(error or None)
            )
        finally:
            proc.kill()

    @classmethod
    def _validate_checker_func(cls, checker_func: str):
        if not checker_func.startswith(
            'def checker(right_value: str, value: str) -> bool:'
        ):
            raise exceptions.CheckerException(messages.MSG_2)
        if checker_func.find('return') < 0:
            raise exceptions.CheckerException(messages.MSG_3)

    @classmethod
    def _check(cls, checker_func: str, **checker_func_vars) -> bool:
        cls._validate_checker_func(checker_func)
        try:
            exec(
                checker_func + '\nresult = checker(right_value, value)',
                globals(),
                checker_func_vars
            )
        except Exception as ex:
            raise exceptions.CheckerException(
                message=messages.MSG_5,
                details=str(ex)
            )
        else:
            result = checker_func_vars['result']
            if not isinstance(result, bool):
                raise exceptions.CheckerException(messages.MSG_4)
            return result

    @classmethod
    def debug(cls, data: DebugData) -> DebugData:
        file = PythonFile(data.code)
        exec_result = cls._execute(
            file=file,
            data_in=data.data_in
        )
        file.remove()
        data.result = exec_result.result
        data.error = exec_result.error
        return data

    @classmethod
    def testing(cls, data: TestsData) -> TestsData:
        file = PythonFile(data.code)
        for test in data.tests:
            exec_result = cls._execute(
                file=file,
                data_in=test.data_in
            )
            test.result = exec_result.result
            test.error = exec_result.error
            test.ok = cls._check(
                checker_func=data.checker,
                right_value=test.data_out,
                value=test.result
            )
        file.remove()
        return data
