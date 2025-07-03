from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field

# 定义一个泛型类型，用于data字段
T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """
    统一API响应模型
    """
    code: int = Field(..., description="业务状态码，例如 200 表示成功")
    message: str = Field(..., description="响应消息，成功或失败的描述")
    data: Optional[T] = Field(None, description="响应数据")

# 预定义一些常用的成功和错误响应
class SuccessResponse(ApiResponse[T]):
    code: int = 200
    message: str = "操作成功"

class BadRequestResponse(ApiResponse[Any]):
    code: int = 400
    message: str = "请求参数错误"

class UnauthorizedResponse(ApiResponse[Any]):
    code: int = 401
    message: str = "认证失败"

class NotFoundResponse(ApiResponse[Any]):
    code: int = 404
    message: str = "资源未找到"

class InternalServerErrorResponse(ApiResponse[Any]):
    code: int = 500
    message: str = "服务器内部错误"