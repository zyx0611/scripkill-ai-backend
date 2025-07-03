from typing import Optional, ClassVar, Type, Any
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import Field
from beanie import Document as BeanieDocument, Indexed
from beanie import Insert, before_event
import uuid


def generate_uuid(length=30):
    """生成指定长度的UUID"""
    # 使用uuid4生成随机uuid
    random_uuid = str(uuid.uuid4()).replace("-", "")
    # 使用截取的方式确保总长度为指定长度
    return random_uuid[:length]


class BaseDocument(BeanieDocument):
    """所有文档模型的基类"""
    # 添加uuid字段并设置唯一索引
    uuid: Indexed(str, unique=True) = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        use_state_management = True
        abstract = True
        
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    
    # 添加before_event钩子，在插入前自动设置uuid的值
    @before_event(Insert)
    def set_uuid(self):
        """在插入文档前自动设置uuid字段的值"""
        if not self.uuid:  # 如果uuid为空，则自动生成
            self.uuid = generate_uuid(30)