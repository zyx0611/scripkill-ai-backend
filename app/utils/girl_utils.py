from app.schemas.girl import GirlResponse, GoodsResponse
from app.models.girl import Girl, Goods


async def create_goods_response(goods: Goods) -> GoodsResponse:
    """根据Goods对象创建GoodsResponse"""
    goods_dict = goods.model_dump()
    temp_dict = goods.template.model_dump(exclude={"id", "uuid", "created_at", "updated_at", "is_active", "match_girl_template_id"})
    return GoodsResponse(**goods_dict, **temp_dict)


async def create_girl_response(girl: Girl) -> GirlResponse:
    """根据Girl对象和物品字典创建GirlResponse"""

    clothes_responses = [await create_goods_response(goods) for goods in girl.clothes]
    jewelry_responses = [await create_goods_response(goods) for goods in girl.jewelrys]
    other_responses = [await create_goods_response(goods) for goods in girl.others]
    dances_responses = [await create_goods_response(goods) for goods in girl.dances]
    clothes_responses.sort(key=lambda x: not x.is_show)
    jewelry_responses.sort(key=lambda x: not x.is_show)
    other_responses.sort(key=lambda x: not x.is_show)
    dances_responses.sort(key=lambda x: not x.is_show)

    girl_dict = girl.model_dump(exclude={"clothes", "jewelrys", "others", "dances"})
    temp_dict = girl.template.model_dump(exclude={"id", "uuid", "created_at", "updated_at", "is_active", "sort"})
    return GirlResponse(
        **girl_dict,
        **temp_dict,
        clothes=clothes_responses,
        jewelrys=jewelry_responses,
        others=other_responses,
        dances=dances_responses
    )