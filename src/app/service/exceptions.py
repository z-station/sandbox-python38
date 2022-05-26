from typing import Optional, Any
from app.service import messages


class ServiceException(Exception):

    default_message = None

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Any] = None
    ):
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class TimeoutException(ServiceException):

    default_message = messages.MSG_1


class CheckerException(ServiceException):

    default_message = messages.MSG_5


class ExecutionException(ServiceException):

    default_message = messages.MSG_6
