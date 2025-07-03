from faulthandler import is_enabled
from typing import Optional, List
from pydantic import Field
from beanie import Indexed, Link, Insert, after_event
from .base import BaseDocument
from .girl import Girl, Goods
from .template import GirlTemplate, GoodsTemplate
from app.logger import getLogger

logger = getLogger(__name__)

class Order(BaseDocument):
    obj_type: str
    obj_id: str
    buy_type: str
    buy_price: int
    is_paid: bool = False
    class Settings:
        name = "orders"
        lookup_field = "uuid"

class User(BaseDocument):
    tg_id: Indexed(str, unique=True) = Field(..., min_length=6, max_length=32)  # tg id
    tg_hash: Optional[str] = None  # tg hash
    username: str = Field(..., min_length=1, max_length=50)  # 用户名
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    avatar_url: Optional[str] = None  # 头像
    bio: Optional[str] = Field(None, max_length=500)  # 简介
    vip_level: int = Field(default=1, ge=1, le=10)  # VIP等级
    gold_coins: int = Field(default=0, ge=0, le=10000)  # 金币
    diamond_coins: int = Field(default=0, ge=0, le=10000)  # 钻石
    girls: List[Link[Girl]] = Field(default_factory=list)
    orders: List[Link[Order]] = Field(default_factory=list)

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "novelist123",
                "is_active": True,
                "bio": "热爱剧本杀的玩家",
            }
        }

    @after_event(Insert)
    async def create_default_girls_and_goods(self):
        """在用户创建后自动创建默认的女孩和物品"""
        # 获取所有is_active为true的GirlTemplate
        logger.info(f"开始为用户 {self.uuid} 创建默认女孩和物品")
        girl_templates = await GirlTemplate.find(
            GirlTemplate.is_active == True
        ).to_list()

        girls = []
        for girl_template in girl_templates:
            # 创建Girl对象
            is_open = (
                True
                if girl_template.open_if == "gold_coins"
                and girl_template.open_number == 0
                else False
            )
            girl = Girl(
                template_id=str(girl_template.uuid),
                user_id=self.uuid,
                is_open=is_open,
                upgrade_value=1000,
                template=girl_template,  # 设置Link关系
            )
            await girl.insert()

            # 为女孩创建各类物品
            for goods_type in Girl.goods_types():
                created_goods = await create_goods_for_girl(
                    goods_type, girl.uuid, self.uuid, girl_template.uuid
                )

                # 根据物品类型更新 Girl 对象的相应字段
                if goods_type == Girl.GOODS_TYPE_CLOTHES:
                    girl.clothes = created_goods
                elif goods_type == Girl.GOODS_TYPE_JEWELRY:
                    girl.jewelrys = created_goods
                elif goods_type == Girl.GOODS_TYPE_OTHER:
                    girl.others = created_goods
                elif goods_type == Girl.GOODS_TYPE_DANCE:
                    girl.dances = created_goods

            # 统一保存更新后的 Girl 对象
            await girl.save()
            girls.append(girl)
        # 更新用户的 girls 字段
        self.girls = girls
        await self.save()


# 创建女友相关
async def create_goods_for_girl(
    goods_type: str, girl_id: str, user_id: str, template_id: str = None
):
    """创建指定类型的物品并返回它们的对象列表"""
    query = {"goods_type": goods_type, "is_active": True}

    # 如果提供了女友模板ID，则筛选匹配的物品
    if goods_type == Girl.GOODS_TYPE_DANCE:
        query["match_girl_template_id"] = template_id

    templates = await GoodsTemplate.find(query).to_list()

    created_goods = []
    for template in templates:
        goods = Goods(
            template_id=str(template.uuid),
            girl_id=girl_id,
            user_id=user_id,
            template=template,  # 设置Link关系
        )
        await goods.insert()
        created_goods.append(goods)

    return created_goods
