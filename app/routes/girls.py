
from fastapi import APIRouter, Depends, HTTPException, params, status
from app.models.template import GirlTemplate, GoodsTemplate
from app.models.user import User
from app.models.girl import Goods, Girl
from app.schemas.girl import GirlResponse, GirlRequest
from app.auth import get_current_user
from app.utils.girl_utils import create_girl_response
from typing import List
from app.schemas.base_api_response import SuccessResponse, NotFoundResponse
from app.utils.user import user_order_create

router = APIRouter()

# 获取当前用户的所有Girl对象
@router.get("/girls", response_model=SuccessResponse[List[GirlResponse]], summary="获取女友列表")
async def get_girls(current_user: User = Depends(get_current_user)):
    """获取当前用户的所有Girl对象"""

    girls = current_user.girls
    # sorted_girls = sorted(girls, key=lambda girl: not girl.is_show)
    sorted_girls = sorted(girls, key=lambda girl: girl.template.sort if girl.template else 0)
    girl_responses = []
    for girl in sorted_girls:
        girl_response = await create_girl_response(girl)
        girl_responses.append(girl_response)
    
    return SuccessResponse(data=girl_responses) 

@router.get("/girls/{girl_uuid}", response_model=SuccessResponse[GirlResponse], summary="获取某个女友信息")
async def get_girl(girl_uuid: str, current_user: User = Depends(get_current_user)):
    """获取当前用户的指定Girl对象"""
    girls = current_user.girls
    girl = next((g for g in girls if g.uuid == girl_uuid), None)
    if not girl:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未找到该女友"))

    girl_response = await create_girl_response(girl)
    return SuccessResponse(data=girl_response)


# 更新指定的Girl对象
@router.post("/girls/{girl_uuid}", summary="更新某个女友信息")
async def get_girl(girl_uuid: str, update_data: GirlRequest, current_user: User = Depends(get_current_user)):
    """更新指定的girl对象"""
    # 查找当前用户的指定Girl对象， 缓存link对象
    girl = await Girl.find_one(Girl.uuid == girl_uuid, fetch_links=True)
    if not girl:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未找到该女友"))
    if girl.user_id != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未找到该女友"))
    if update_data.is_show is not None:
        if girl.is_open == False:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="该女友未解锁"))
        girl.is_show = update_data.is_show
        await girl.save()
        # if true 关闭其他女友
        if girl.is_show == True:
            girls: Girl = current_user.girls
            for g in girls:
                if g.uuid != girl_uuid:
                    g.is_show = False
                    await g.save()
    if update_data.is_open == True:
        # 条件满足解锁女友
        if girl.is_open:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="该女友已经解锁"))
        open_if = girl.template.open_if
        open_number = girl.template.open_number
        if open_if == "gold_coins":
            if current_user.gold_coins < open_number:
                raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="金币不足"))
            current_user.gold_coins -= open_number
        elif open_if == "diamond_coins":
            if current_user.diamond_coins < open_number:
                raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="钻石不足"))
            current_user.diamond_coins -= open_number
        else:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未知的开放条件"))
        await current_user.save()
        girl.is_open = True
        await girl.save()
        await user_order_create(current_user, girl)
    return SuccessResponse()

@router.get("/goods", response_model=SuccessResponse[GirlResponse], summary="获取女友穿搭列表")
async def get_girl(girl_uuid: str, current_user: User = Depends(get_current_user)):
    """获取所有衣服/饰品/其他物品"""
    girls = current_user.girls
    girl = next((g for g in girls if g.uuid == girl_uuid), None)
    if not girl:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未找到该女友"))

    girl_response = await create_girl_response(girl)
    return SuccessResponse(data=girl_response)

# 更新指定的Goods对象
@router.post("/goods/{goods_uuid}", summary="更新女友穿搭信息")
async def get_girl(goods_uuid: str, update_data: GirlRequest, current_user: User = Depends(get_current_user)):
    """更新指定的Goods对象"""
    # 查找当前用户的指定Goods对象
    goods = await Goods.find_one(Goods.uuid == goods_uuid, fetch_links=True)
    if not goods:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未找到该物品"))
    if goods.user_id != current_user.uuid:
        raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未找到该物品"))

    if update_data.is_show is not None:
        if goods.is_open == False:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="该物品未解锁"))
        goods.is_show = update_data.is_show
        await goods.save()
        # girl = await Girl.find_one(Girl.uuid == goods.girl_id, fetch_links=True)
        all_goods = await Goods.find(Goods.girl_id == goods.girl_id, fetch_links=True).to_list()
        for g in all_goods:
            if g.uuid!= goods_uuid and g.template.is_active == True and g.template.goods_type == goods.template.goods_type:
                g.is_show = False
                await g.save()
    if update_data.is_open == True:
        # 条件满足解锁女友
        if goods.is_open:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="该物品已经解锁"))
        open_if = goods.template.open_if
        open_number = goods.template.open_number
        if open_if == "gold_coins":
            if current_user.gold_coins < open_number:
                raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="金币不足"))
            current_user.gold_coins -= open_number
        elif open_if == "diamond_coins":
            if current_user.diamond_coins < open_number:
                raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="钻石不足"))
            current_user.diamond_coins -= open_number
        else:
            raise HTTPException(status_code=status.HTTP_200_OK, detail=NotFoundResponse(message="未知的开放条件"))
        await current_user.save()
        goods.is_open = True
        await goods.save()
        await user_order_create(current_user, goods)
    return SuccessResponse()