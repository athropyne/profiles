from sqlalchemy import Table, Column, String, MetaData, Integer, BIGINT

from models import ProfileAliases

metadata = MetaData()

profiles = Table(
    "профили",
    metadata,
    Column(ProfileAliases.ID, Integer, unique=True, nullable=False),
    Column(ProfileAliases.GAME_ID, BIGINT, nullable=False),
    Column(ProfileAliases.GAME_NICKNAME, String(30), nullable=False)
)
