from typing import Any
import requests
from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.models.user import User
from app.models.girl import Girl
from app.schemas.user import UserResponse, TokenResponse, UserCreate, GirlInfoResponse
from app.auth import create_access_token, get_current_user
import logging
from app.schemas.base_api_response import InternalServerErrorResponse, SuccessResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=SuccessResponse[Any])
async def login(user_create: UserCreate, response: Response):
    def getCookie(username: str = 'default-user', password: str = '12345678'):
        res = requests.post('http://localhost:8000//api/users/login', json={
            "handle": username,
            "password": password
        }, headers={
            "x-csrf-token": "disabled"
        })
        if res.status_code == 200:
            cookies = res.cookies
            cookie_header_str = '; '.join([f"{c.name}={c.value}" for c in cookies])
            return cookie_header_str
        else:
            raise HTTPException(status_code=500, detail="登陆接口请求失败")

    def createdCharactersAndChat(token: json):
        charactersBody = {

        }
        res = requests.post("http://localhost:8000/api/characters/create", json=charactersBody, headers=token)

    """注册用户"""
    # 检查用户是否已存在
    existing_user = await User.find_one(User.tg_id == user_create.tg_id)
    if existing_user:
        token = getCookie(existing_user.username)
        await existing_user.set({"cookie": token})
        response.set_cookie(
            key="access_token",
            value=token
        )
        return SuccessResponse(data=create_access_token(data={"sub": existing_user.uuid}))

    # 创建新用户
    user = User(**user_create.model_dump())
    user.gold_coins = 20
    defaultUserToken = getCookie()
    new_user = requests.post('http://localhost:8000/api/users/create', json={
        'handle': user_create.username,
        'name': user_create.username,
        'password': '12345678'
    }, headers={
        "cookie": defaultUserToken
    })
    try:
        existing_user = await user.insert()
        token = getCookie(user_create.username)
        response.set_cookie(
            key="access_token",
            value=token
        )
        return SuccessResponse(data=create_access_token(data={"sub": existing_user.uuid}))
    except Exception as e:
        logger.error(f"Failed to register user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=InternalServerErrorResponse().model_dump()
        )

@router.get("/me", response_model=SuccessResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    girls = current_user.girls
    # sorted_girls = sorted(girls, key=lambda girl: girl.template.sort if girl.template else 0)
    sorted_girls = sorted(girls, key=lambda girl: not girl.is_show)

    girl_responses = []
    for girl in sorted_girls:
        girl_dict = girl.model_dump()
        temp_dict = girl.template.model_dump(exclude={"id", "uuid", "created_at", "updated_at", "is_active", "sort"})
        for dance in girl.dances:
            if dance.is_show:
                temp_dict['pic'] = dance.template.pic
                break
        girl_response = GirlInfoResponse(**girl_dict, **temp_dict)
        girl_responses.append(girl_response)
    
    # 构建并返回UserResponse
    user_data = current_user.model_dump()
    user_data["girls"] = girl_responses
    return SuccessResponse(data=UserResponse(**user_data))