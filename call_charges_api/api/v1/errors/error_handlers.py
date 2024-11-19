from fastapi import HTTPException

from call_charges_api.domain.errors.exceptions import (
    BusinessException,
    InvalidCredentialsException,
    InvalidPhoneNumberException,
    ReferencePeriodFormatException,
    StartRecordNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


def handle_error(exception: Exception) -> HTTPException:
    exception_map = {
        InvalidPhoneNumberException: (400, 'InvalidPhoneNumber'),
        StartRecordNotFoundException: (404, 'StartCallRecordNotFound'),
        BusinessException: (422, 'BusinessException'),
        ReferencePeriodFormatException: (
            422,
            'ReferencePeriodFormatException',
        ),
        UserNotFoundException: (404, 'UserNotFound'),
        UserAlreadyExistsException: (409, 'UserAlreadyExists'),
        InvalidCredentialsException: (401, 'InvalidCredentials'),
    }

    for exc_type, (status_code, error) in exception_map.items():
        if isinstance(exception, exc_type):
            return HTTPException(
                status_code=status_code,
                detail={
                    'error': error,
                    'message': exception.message,
                },
            )

    return HTTPException(
        status_code=500,
        detail={
            'error': 'InternalServerError',
            'message': 'Oops! An unexpected error occurred.',
        },
    )
