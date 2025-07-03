from pydantic import Field
from .base import BaseDocument
from typing import Optional


class GirlTemplate(BaseDocument):
    name: str = ""
    age: int = 0 # 年龄
    height: int = 0 # 身高
    job: str = "" # 职业
    pic: str # 图片或视频
    sort: int = 0 # 排序
    open_if: str = Field(default="gold_coins") # 解锁所需的条件
    open_number: int = 0 # 解锁所需的数量
    is_active: bool = Field(default=True) # 是否激活
    
    class Settings:
        name = "girl_templates"
        # lookup_field = "uuid"


class GoodsTemplate(BaseDocument):
    name: str = ""
    pic: str # 图片或视频
    goods_type: str = "" # 商品类型
    open_if: str = Field(default="gold_coins") # 打开所需的条件
    open_number: int = 0 # 打开所需的数量
    is_active: bool = Field(default=True) # 是否激活
    match_girl_template_id: Optional[str] = None # 专属女友物品 模板ID
    
    class Settings:
        name = "goods_templates"
        lookup_field = "uuid"