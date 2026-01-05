from fastapi import FastAPI
from database import delete_tables, create_tables
from router import router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print('База очищена')
    await create_tables()
    print('База готова')
    yield
    print('Выключение...')

app = FastAPI(lifespan=lifespan)
app.include_router(router)
