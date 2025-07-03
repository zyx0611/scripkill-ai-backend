from typing import List, Optional, ClassVar
from pydantic import Field
from beanie import Indexed, Link
from .base import BaseDocument
from .template import GoodsTemplate, GirlTemplate

class Goods(BaseDocument):
    is_show: bool = Field(default=False)
    is_open: bool = Field(default=False)
    girl_id: str = ""
    template_id: str = ""
    user_id: str = ""

    template: Link[GoodsTemplate] = None
    
    class Settings:
        name = "goods"
        lookup_field = "uuid"
    
    # async def get_girl(self):
    #     return await Girl.find(Girl.clothes.id == self.uuid).to_list()



class Girl(BaseDocument):
    # 定义物品类型常量
    GOODS_TYPE_CLOTHES: ClassVar[str] = "clothes"
    GOODS_TYPE_JEWELRY: ClassVar[str] = "jewelrys"
    GOODS_TYPE_OTHER: ClassVar[str] = "others"
    GOODS_TYPE_DANCE: ClassVar[str] = "dances"
    
    @classmethod
    def goods_types(cls) -> List[str]:
        return [cls.GOODS_TYPE_CLOTHES, cls.GOODS_TYPE_JEWELRY, cls.GOODS_TYPE_OTHER, cls.GOODS_TYPE_DANCE]
    
    template_id: str = ""
    user_id: str = ""
    is_show: bool = Field(default=False) # 是否显示
    is_open: bool = Field(default=False) # 是否开启
    level: int = Field(default=1)
    upgrade_value: int = Field(default=1000) # 升级所需的经验值
    current_upgrade_value: int = Field(default=0)

    template: Link[GirlTemplate] = None # 女友模板
    clothes: List[Link[Goods]] = [] # 服装
    jewelrys: List[Link[Goods]] = [] # 饰品
    others: List[Link[Goods]] = [] # 其他
    dances: List[Link[Goods]] = [] # 舞蹈

    
    class Settings:
        name = "girls"
        lookup_field = "uuid"


