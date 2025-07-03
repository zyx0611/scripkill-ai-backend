from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, girls, scripts, games, chat
from app.init_db import init_db
from app.config import settings
from fastapi.exceptions import RequestValidationError
from app.schemas.base_api_response import BadRequestResponse
from pydantic import ValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 连接数据库并初始化Beanie
    client = await connect_to_mongo()
    # 初始化数据库数据
    await init_db()
    yield
    # 关闭数据库连接
    await close_mongo_connection(client)


app = FastAPI(
    title=settings.app_name,
    description=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


# 验证错误异常处理器
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=200,
        content={"code": 400, "message": "数据验证错误", "errors": exc.errors()},
    )


# 添加请求验证异常处理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    # 返回BadRequestResponse
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=BadRequestResponse(data=exc.errors()).model_dump(),
    )


# 添加异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # 检查 detail 是否为 Pydantic 模型或字典
    if hasattr(exc.detail, "model_dump"):
        detail = exc.detail.model_dump()
    else:
        detail = exc.detail

    if isinstance(detail, dict) and "code" in detail and "message" in detail:
        return JSONResponse(status_code=exc.status_code, content=detail)
    # 否则创建一个新的 ApiResponse
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": str(detail), "data": None},
    )


# 跨域设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(girls.router, prefix="/api/v1", tags=["girls"])
app.include_router(scripts.router, prefix="/api/v1", tags=["scripts"])
app.include_router(games.router, prefix="/api/v1", tags=["games"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])


@app.get("/")
async def root():
    return {"message": "剧本杀系统API服务正在运行"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
