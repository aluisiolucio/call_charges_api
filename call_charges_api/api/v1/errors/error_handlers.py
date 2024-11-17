from fastapi import HTTPException

from call_charges_api.domain.errors.exceptions import (
    BusinessException,
    InvalidPhoneNumberException,
    StartRecordNotFoundException,
)


def handle_error(exception: Exception) -> HTTPException:
    if isinstance(exception, InvalidPhoneNumberException):
        return HTTPException(
            status_code=400,
            detail={
                'error': 'InvalidPhoneNumber',
                'message': exception.message,
            },
        )

    if isinstance(exception, StartRecordNotFoundException):
        return HTTPException(
            status_code=404,
            detail={
                'error': 'StartCallRecordNotFound',
                'message': exception.message,
            },
        )

    if isinstance(exception, BusinessException):
        return HTTPException(
            status_code=422,
            detail={
                'error': 'BusinessException',
                'message': exception.message,
            },
        )

    return HTTPException(
        status_code=500,
        detail={
            'error': 'InternalServerError',
            'message': 'Oops! An unexpected error occurred. '
            'Please try again later.',
        },
    )
