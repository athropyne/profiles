import dataclasses
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from sqlalchemy import String, Integer, DATETIME


@dataclasses.dataclass
class ProfileAliases:
    ID = "идентификатор"
    GAME_ID = "ид в игре"
    GAME_NICKNAME = "ник в игре"


class NewProfileModel(BaseModel):
    ID: int = Field(alias=ProfileAliases.ID)
    game_id: int = Field(alias=ProfileAliases.GAME_ID)
    game_nickname: str = Field(max_length=30, alias=ProfileAliases.GAME_NICKNAME)


class UpdateProfileModel(BaseModel):
    game_id: Optional[int] = Field(alias=ProfileAliases.GAME_ID)
    game_nickname: Optional[str] = Field(max_length=30, alias=ProfileAliases.GAME_NICKNAME)


