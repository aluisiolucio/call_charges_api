from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from call_charges_api.api.v1.errors.error_handlers import handle_error
from call_charges_api.api.v1.schemas.call_record import (
    RequestSchema,
    ResponseSchema,
)
from call_charges_api.domain.use_cases.register_call import (
    Input as RegisterCallInput,
)
from call_charges_api.domain.use_cases.register_call import (
    RegisterCallUseCase,
)
from call_charges_api.infra.db.session import get_session
from call_charges_api.infra.sqlalchemy_repos.sqlalchemy_call_record_repository import (  # noqa: E501
    SQLAlchemyCallRecordRepository,
)

router = APIRouter(prefix='/api/v1', tags=['call_records'])


@router.put(
    '/call_records',
    status_code=HTTPStatus.CREATED,
    response_model=ResponseSchema,
)
def register_call(
    call_record_schema: RequestSchema, session: Session = Depends(get_session)
):
    repo = SQLAlchemyCallRecordRepository(session)
    use_case = RegisterCallUseCase(repo)

    try:
        record = use_case.execute(
            RegisterCallInput(
                call_type=call_record_schema.type,
                timestamp=call_record_schema.timestamp,
                call_id=call_record_schema.call_id,
                source=call_record_schema.source,
                destination=call_record_schema.destination,
            )
        )

        return ResponseSchema(
            id=record.id,
            type=record.call_type,
            timestamp=record.timestamp,
            call_id=record.call_id,
            source=record.source,
            destination=record.destination,
        )
    except Exception as e:
        print(e)
        raise handle_error(e)
