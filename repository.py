from database import new_session, UserOrm, PostsOrm
from sqlalchemy import select
from auth import create_access_token, decode_token
from fastapi import HTTPException
from schemas import Role
from config import settings


class TaskReposytory():
    @classmethod
    async def SignIn(cls, user):
        async with new_session() as session:
            user_dict = user.model_dump()
            model = UserOrm(**user_dict)
            model.role = Role.USER
            session.add(model)
            await session.flush()
            await session.commit()
            await session.refresh(model)

            return create_access_token(model)
        
    @classmethod
    async def GetUsers(cls):
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            model = result.scalars().all()
            return model
    
    @classmethod
    async def DeleteUser(cls, user_id, password):
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            model = result.scalar_one()
            if model.password != password:
                raise HTTPException(status_code=404, detail="Неверный пароль")
            
            await session.delete(model)
            await session.commit()

    @classmethod
    async def CreatePost(cls, post, user_id):
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            user_model = result.scalar_one()
            if user_model.role != Role.USER:
                raise HTTPException(status_code=403, detali="Недостаточно прав")
            post_dict = post.model_dump()
            model = PostsOrm(**post_dict)
            model.username = user_model.username
            model.role = user_model.role
            session.add(model)
            await session.flush()
            await session.commit()
            await session.refresh(model)

    @classmethod
    async def GetPosts(cls):
        async with new_session() as session:
            query = select(PostsOrm)
            result = await session.execute(query)
            model = result.scalars().all()
            return model
        
    @classmethod
    async def AdminStatus(cls, user_id, password):
        async with new_session() as session:
            if password != settings.admin_password:
                raise HTTPException(status_code=404)
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            model = result.scalar_one()
            model.role = Role.ADMIN
            await session.commit()
            await session.refresh(model)

            return create_access_token(model)
        
    @classmethod
    async def GiveModerator(cls, user_id, token):
        async with new_session() as session:
            user_token = decode_token(token, settings.access_cookie_name)
            if user_token.role != "admin":
                raise HTTPException(status_code=403)
            
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            model = result.scalar_one()
            model.role = Role.MODERATER
            await session.commit()
            await session.refresh(model)
        



            