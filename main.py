import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import ALLOW_ORIGINS
from database import engine
from routes import router
from schemas import metadata

app = FastAPI(title="профили")
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    try:
        async with engine.connect() as connection:
            await connection.run_sync(metadata.create_all)
            await connection.commit()
        await engine.dispose()
    except OSError as e:
        print("ошибка подключения к базе данных")
        print(e)



if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        port=8002,
        reload=True
    )
