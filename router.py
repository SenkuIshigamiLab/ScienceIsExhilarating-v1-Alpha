from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import Annotated
from repository import TaskReposytory
from schemas import UserLogin, Post, UserPost
from auth import decode_token
from config import settings

router = APIRouter(
    prefix="/task"
)

security = HTTPBearer()

def getcurrentuser(token: str = Depends(security)):
    token = decode_token(token, settings.access_cookie_name)
    return token

@router.post("/authorization")
async def SignIn(user: Annotated[dict, Depends(UserLogin)]):
    UserToken = await TaskReposytory.SignIn(user)
    return UserToken

@router.get("/getUsers")
async def GetUsers():
    users = await TaskReposytory.GetUsers()
    return users

@router.delete("/deleteAccount")
async def DeleteUser(user_id: int, password: str):
    delete = await TaskReposytory.DeleteUser(user_id, password)
    return delete

@router.post("/addPost")
async def CreatePost(post: Post, user_id: int):
    Post = await TaskReposytory.CreatePost(post, user_id)
    return Post

@router.post("/getAllPosts")
async def GetPosts() -> list[UserPost]:
    Posts = await TaskReposytory.GetPosts()
    return Posts

@router.patch("/getAdminStatus")
async def AdminStatus(user_id: int, password: str):
    UserAdmin = await TaskReposytory.AdminStatus(user_id, password)
    return UserAdmin

@router.patch("/giveModeratorStatus")
async def ModeratorStatud(user_id: int, token: str = Depends(getcurrentuser)):
    Moderator = await TaskReposytory.GiveModerator(user_id, token)
    return Moderator