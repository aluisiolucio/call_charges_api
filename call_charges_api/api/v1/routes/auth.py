from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from call_charges_api.api.v1.errors.error_handlers import handle_error
from call_charges_api.api.v1.schemas.auth import TokenOutputSchema
from call_charges_api.api.v1.schemas.user import (
    UserInputSchema,
    UserOutputSchema,
)
from call_charges_api.domain.use_cases.auth import (
    AuthInput,
    SignInUseCase,
    SignUpUseCase,
)
from call_charges_api.infra.db.session import get_session
from call_charges_api.infra.sqlalchemy_repos.sqlalchemy_user_repository import (  # noqa: E501
    SQLAlchemyUserRepository,
)

router = APIRouter(tags=['auth'])


@router.post(
    '/register',
    status_code=HTTPStatus.CREATED,
    response_model=UserOutputSchema,
)
def sign_up(
    user_schema: UserInputSchema, session: Session = Depends(get_session)
):
    repo = SQLAlchemyUserRepository(session)
    use_case = SignUpUseCase(repo)

    try:
        user = use_case.execute(
            AuthInput(
                username=user_schema.username,
                password=user_schema.password,
            )
        )

        return UserOutputSchema(id=user.id, username=user.username)
    except Exception as e:
        print(e)
        raise handle_error(e)


@router.post('/token', response_model=TokenOutputSchema)
def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    repo = SQLAlchemyUserRepository(session)
    use_case = SignInUseCase(repo)

    try:
        token = use_case.execute(
            AuthInput(
                username=form_data.username,
                password=form_data.password,
            )
        )

        return TokenOutputSchema(
            id=token.id,
            username=token.username,
            access_token=token.access_token,
            token_type=token.token_type,
        )
    except Exception as e:
        print(e)
        raise handle_error(e)
