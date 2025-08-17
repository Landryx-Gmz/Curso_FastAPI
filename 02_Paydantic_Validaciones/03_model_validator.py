# After
# Before
# Wrap
# Para modelos no tiene el modo Plain

from typing_extensions import Self
from pydantic import BaseModel, model_validator

class UserModel(BaseModel):
    username: str
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Objeto incorrecto, passwords no match")
        return self

usuario1: UserModel = UserModel(username="Andy", password="1234", password_repeat="12345")