from uuid import uuid4

from sqlalchemy import select

from call_charges_api.infra.models.user import UserModel
from call_charges_api.repositories.user_repository import (  # noqa: E501
    UserInput,
    UserOutput,
    UserRepository,
)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self._session = session

    def save(self, user_input: UserInput) -> UserOutput | str:
        user_db = self._session.scalar(
            select(UserModel).where(UserModel.username == user_input.username)
        )

        if user_db:
            return 'User already exists'

        user_db = UserModel(
            id=uuid4(),
            username=user_input.username,
            password=user_input.password,
        )

        self._session.add(user_db)
        self._session.commit()
        self._session.refresh(user_db)

        return UserOutput(
            id=user_db.id,
            username=user_db.username,
        )

    def get_by_username(self, username: str) -> UserOutput | None:
        user_db = self._session.scalar(
            select(UserModel).where(UserModel.username == username)
        )

        if not user_db:
            return None

        return UserOutput(
            id=user_db.id,
            username=user_db.username,
            password=user_db.password,
        )
