from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

engine = create_async_engine(
    "sqlite+aiosqlite:///ScienceIsExhilarating.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class UserOrm(Model):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]

class PostsOrm(Model):
    __tablename__ = "Posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    role: Mapped[str]
    text: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
