from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from call_charges_api.domain.errors.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from call_charges_api.infra.config.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from call_charges_api.repositories.user_repository import (
    UserInput,
    UserRepository,
)


@dataclass
class AuthInput:
    username: str
    password: str


@dataclass
class AuthOutput:
    id: UUID
    username: str
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class SignInUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, input: AuthInput) -> AuthOutput:
        user = self.repository.get_by_username(input.username)

        if not user:
            raise UserNotFoundException(input.username)

        if not verify_password(input.password, user.password):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            data={
                'uid': str(user.id),
                'sub': user.username,
            }
        )

        return AuthOutput(
            id=user.id,
            username=user.username,
            access_token=access_token,
            token_type='bearer',
        )


class SignUpUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, input: AuthInput) -> AuthOutput:
        hashed_password = get_password_hash(input.password)

        user_input = UserInput(
            username=input.username,
            password=hashed_password,
        )

        user_output = self.repository.save(user_input)

        if isinstance(user_output, str):
            raise UserAlreadyExistsException(user_input.username)

        return AuthOutput(
            id=user_output.id,
            username=user_output.username,
        )


class RefreshTokenUseCase:
    @staticmethod
    def execute(id: UUID, username: str) -> AuthOutput:
        access_token = create_access_token(
            data={
                'uid': str(id),
                'sub': username,
            }
        )

        return AuthOutput(
            id=id,
            username=username,
            access_token=access_token,
            token_type='bearer',
        )
