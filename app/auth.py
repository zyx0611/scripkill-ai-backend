from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings
from app.schemas.user import TokenData, TokenResponse
from app.models.user import User  # 导入 User 模型
from bson import ObjectId
from app.schemas.base_api_response import NotFoundResponse, UnauthorizedResponse

from app.logger import getLogger
logger = getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")
security = HTTPBearer(auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return TokenResponse(access_token=encoded_jwt, expired_at=int(expire.timestamp()))


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=UnauthorizedResponse().model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    
    if not credentials:
        raise credentials_exception
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        uuid: str = payload.get("sub")
        if uuid is None:
            raise credentials_exception
        token_data = TokenData(uuid=uuid)
    except JWTError as e:
        logger.error(f"JWT decode error: {e}")
        raise credentials_exception
        
    # 使用 Beanie 查询用户，并预加载girls字段fetch_links
    user = await User.find_one(User.uuid == token_data.uuid, fetch_links=True)
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=NotFoundResponse(message="用户被禁止登录")
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=NotFoundResponse(message="用户被禁止登录")
        )
    return current_user