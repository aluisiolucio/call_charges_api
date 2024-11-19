from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class UserInput:
    username: str
    password: str


@dataclass
class UserOutput:
    id: UUID
    username: str
    password: Optional[str] = None


class UserRepository:
    def save(self, user_input: UserInput) -> UserOutput | str:
        raise NotImplementedError

    def get_by_username(self, username: str) -> UserOutput | None:
        raise NotImplementedError
