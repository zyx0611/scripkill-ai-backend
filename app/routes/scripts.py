# routers/scripts.py

from fastapi import APIRouter, HTTPException, status
from typing import List

from app.models.script import Script
from app.schemas.script import ScriptCreate, ScriptResponse
from app.models.script import ContentPart, Character
from app.schemas.base_api_response import SuccessResponse, NotFoundResponse

router = APIRouter()

@router.post(
    "/scripts",
    status_code=status.HTTP_201_CREATED,
    summary="创建一个新剧本"
)
async def create_script(script_data: ScriptCreate):
    """创建一个新的剧本杀"""
    collection = Script.get_motor_collection()
    existing_script = await collection.find_one({"title": script_data.title})
    if existing_script:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"this title script kill already exists"
        )
    
    new_script = Script(**script_data.model_dump())
    data = await new_script.create()
    return SuccessResponse()

@router.get(
    "/scripts",
    response_model=SuccessResponse[List[ScriptResponse]],
    summary="剧本列表"
)
async def get_scripts():
    scripts = await Script.all().sort([("score", -1)]).to_list()
    return SuccessResponse(data=scripts)


@router.get(
    "/scripts/{script_id}/content",
    response_model=SuccessResponse[List[ContentPart]],
    summary="根据ID获取剧本正文"
)
async def get_script_by_id(script_id: str):
    script = await Script.find_one(Script.uuid == script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found script"
        )
    return SuccessResponse(data=script.content)

@router.get(
    "/scripts/{script_id}/characters",
    response_model=SuccessResponse[List[Character]],
    summary="根据ID获取剧本角色"
)
async def get_script_by_id(script_id: str):
    script = await Script.find_one(Script.uuid == script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NotFoundResponse(message="该剧本杀未找到")
        )
    return SuccessResponse(data=script.characters)