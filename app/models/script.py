from .base import BaseDocument
from enum import Enum
from typing import List, Optional, Union, Annotated
from beanie import Indexed, Link
from pydantic import BaseModel, Field
from typing_extensions import Literal
from pymongo import IndexModel, TEXT, ASCENDING
from datetime import datetime
from app.models.user import User

class Character(BaseModel):
    """剧本角色"""
    name: str # 角色名称
    relationship: str # 与其他角色的关系
    contradictionPoint: str # 与其他角色的矛盾点
    strs: Optional[str] = None
    words: str # 角色的台词

class TextContentPart(BaseModel):
    """剧情文本部分"""
    # part_id: int
    type: Literal["text"] # 类型为文本
    text: str # 剧情文本

class ClueContentPart(BaseModel):
    """剧情线索部分"""
    # part_id: int
    type: Literal["clue"] # 类型为线索
    clicks: bool = False # 是否可点击
    text: str # 剧情中可点击的文本
    clue_index: int # 关联的线索 ID
    clue_text: str # 点击后展示的线索详情
    suspect_hints: List[str] #针对嫌疑人的线索补充

# 使用 Annotated 和 Field 来正确处理
ContentPart = Annotated[Union[TextContentPart, ClueContentPart], Field(discriminator="type")]

class Solution(BaseModel):
    """剧本答案"""
    murderer_id: str # 凶手 ID
    # motive: str # 动机
    # evidence_chain: str # 证据链

class Script(BaseDocument):
    """剧本模板模型。"""
    title: str # 剧本标题
    description: Optional[str] = "" # 剧本简介
    cover_url: Optional[str] = None # 封面图片 URL
    difficulty_level: int # 难度，如 '简单', '中等', '困难'
    player_count: Optional[int] = None # 玩家人数
    times: Optional[int] = None # 预计游戏时长（分钟）
    score: int # 剧本得分
    characters: List[Character] # 角色列表
    content: List[ContentPart] # 剧本内容
    tags: List[str] = [] # 标签
    # solution: Solution # 答案

    class Settings:
        name = "scripts"
        indexes = [
            IndexModel(["score"], name="score_index"),
            IndexModel([("title", TEXT), ("description", TEXT)], name="title_desc_text_index")
        ]

class GameStatus(str, Enum):
    """游戏状态枚举"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class FinalChoice(BaseModel):
    """玩家最终选择"""
    guessed_murderer_id: Optional[str] = None
    reason: Optional[str] = None
    submission_time: Optional[datetime] = None


class GameScript(BaseDocument):
    """
    游戏会话/进度模型。
    这是动态数据，会频繁更新。通过 Link 关联 User 和 Script。
    """
    user: Link[User] # 关联的用户
    script: Link[Script] # 关联的剧本模板
    
    status: GameStatus = GameStatus.IN_PROGRESS # 游戏状态
    end_time: Optional[datetime] = None # 游戏结束时间
    final_choice: FinalChoice = Field(default_factory=FinalChoice) # 玩家的最终选择
    
    score: int = 0 # 玩家的得分
    is_correct: Optional[bool] = None # 玩家是否猜对了凶手

    class Settings:
        name = "game_scripts"
        indexes = [
            IndexModel([("user._id", ASCENDING)], name="user_id_index"),
            IndexModel([("script._id", ASCENDING)], name="script_id_index"),
            IndexModel([("user._id", ASCENDING), ("script._id", ASCENDING)], name="user_script_compound_index")
        ]