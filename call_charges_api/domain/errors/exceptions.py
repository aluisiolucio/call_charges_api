class BusinessException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidPhoneNumberException(BusinessException):
    def __init__(self, phone_number: str):
        message = f"The phone number '{phone_number}' is invalid."
        super().__init__(message)


class StartRecordNotFoundException(BusinessException):
    def __init__(self, call_id: int):
        message = f'Start call record with ID {call_id} was not found.'
        super().__init__(message)


class ReferencePeriodFormatException(BusinessException):
    def __init__(self):
        message = 'The reference period format is invalid. '
        'Use MM/YY or MM/YYYY.'
        super().__init__(message)


class UserNotFoundException(BusinessException):
    def __init__(self, username: str):
        message = f'User with username {username} was not found.'
        super().__init__(message)


class UserAlreadyExistsException(BusinessException):
    def __init__(self, username: str):
        message = f'User with username {username} already exists.'
        super().__init__(message)


class InvalidCredentialsException(BusinessException):
    def __init__(self):
        message = 'Incorrect email or password'
        super().__init__(message)
