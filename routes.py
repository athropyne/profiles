from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import CursorResult, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status
from starlette.responses import JSONResponse

from database import get_connection
from models import ProfileAliases, NewProfileModel, UpdateProfileModel
from schemas import profiles

router = APIRouter()


@router.post("/")
async def new(
        model: NewProfileModel,
        connection: AsyncConnection = Depends(get_connection)
):
    try:
        cursor: CursorResult = await connection.execute(
            insert(profiles)
            .values(**model.model_dump(by_alias=True))
            .returning(profiles)
        )
        data = cursor.mappings().one_or_none()
        result = data if data is None else jsonable_encoder(dict(data))
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result
        )
    except IntegrityError as e:
        if "already exists" in e.orig.args[0]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="такой идентификатор уже существует"
            )


@router.put("/{ID}")
async def update(
        ID: int,
        model: UpdateProfileModel,
        connection: AsyncConnection = Depends(get_connection)
):
    cursor: CursorResult = await connection.execute(
        profiles
        .update()
        .values(**model.model_dump(by_alias=True))
        .where(profiles.c[ProfileAliases.ID] == ID)
        .returning(profiles)
    )
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="профиль с таким идентификатором не найден"
        )
    data = cursor.mappings().one_or_none()
    result = data if data is None else jsonable_encoder(dict(data))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result
    )


@router.get("/{ID}")
async def get_one(
        ID: int,
        connection: AsyncConnection = Depends(get_connection)
):
    cursor: CursorResult = await connection.execute(
        select(profiles)
        .where(profiles.c[ProfileAliases.ID] == ID)
    )
    data = cursor.mappings().one_or_none()
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="профиль с таким идентификатором не найден"
        )
    result = data if data is None else jsonable_encoder(dict(data))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result
    )


@router.get("/")
async def get_list(
        skip: int = 0,
        limit: int = 20,
        connection: AsyncConnection = Depends(get_connection)
):
    cursor: CursorResult = await connection.execute(
        select(profiles)
        .offset(skip)
        .limit(limit)
    )

    data = cursor.mappings().fetchall()
    result = jsonable_encoder(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result
    )


@router.delete("/{ID}")
async def get_one(
        ID: int,
        connection: AsyncConnection = Depends(get_connection)
):
    cursor: CursorResult = await connection.execute(
        profiles.delete()
        .where(profiles.c[ProfileAliases.ID] == ID)
    )
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="профиль с таким идентификатором не найден"
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="профиль удален"
    )
