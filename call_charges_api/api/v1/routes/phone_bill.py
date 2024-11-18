from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from call_charges_api.api.v1.errors.error_handlers import handle_error
from call_charges_api.api.v1.schemas.phone_bill import (
    FiltersSchema,
    PhoneBillListSchema,
    PhoneBillResponseSchema,
)
from call_charges_api.domain.use_cases.get_phone_bill import (
    GetPhoneBillUseCase,
)
from call_charges_api.domain.use_cases.get_phone_bill import (
    Input as GetPhoneBillInput,
)
from call_charges_api.infra.db.session import get_session
from call_charges_api.infra.sqlalchemy_repos.sqlalchemy_phone_bill_repository import (  # noqa: E501
    SQLAlchemyPhoneBillRepository,
)

router = APIRouter(prefix='/api/v1', tags=['phone_bill'])


@router.get(
    '/phone_bill',
    status_code=HTTPStatus.OK,
    response_model=PhoneBillListSchema,
)
def get_phone_bill(
    phone_bill_filters: Annotated[FiltersSchema, Query()],
    session: Session = Depends(get_session),
):
    try:
        repo = SQLAlchemyPhoneBillRepository(session)
        use_case = GetPhoneBillUseCase(repo)

        bill = use_case.execute(
            GetPhoneBillInput(
                phone_number=phone_bill_filters.phone_number,
                reference_period=phone_bill_filters.reference_period,
            )
        )

        if not bill:
            return PhoneBillListSchema(bills=[])

        bill_schema = PhoneBillResponseSchema(
            id=bill.id,
            phone_number=bill.phone_number,
            reference_period=bill.reference_period,
            total_amount=bill.total_amount,
            call_records=bill.call_records,
        )

        return PhoneBillListSchema(
            bills=[bill_schema],
        )
    except Exception as e:
        print(e)
        raise handle_error(e)
