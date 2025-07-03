from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    tg_id: str
    tg_hash: Optional[str] = None
    avatar_url: Optional[str] = None


class GirlInfoResponse(BaseModel):
    uuid: str
    name: str
    age: int
    height: int
    job: str
    level: int
    pic: str
    is_show: bool
    is_open: bool
    open_if: str
    open_number: int
    upgrade_value: int
    current_upgrade_value: int

class UserResponse(BaseModel):
    uuid: str
    username: str
    is_active: bool
    avatar_url: Optional[str] = None
    tg_id: str
    vip_level: int
    gold_coins: int
    diamond_coins: int
    girls: Optional[list[GirlInfoResponse]] = None
    created_at: datetime



class TokenData(BaseModel):
    uuid: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    expired_at: int
