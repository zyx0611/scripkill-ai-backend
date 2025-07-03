# schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional, Annotated, Union
from datetime import datetime

# Import the individual content part types instead of the combined type
from app.models.script import Character, TextContentPart, ClueContentPart

# Redefine ContentPart with the discriminator applied to the Union
ContentPart = Annotated[Union[TextContentPart, ClueContentPart], Field(discriminator="type")]


class ScriptCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="剧本标题")
    description: Optional[str] = None
    cover_url: Optional[str] = None
    difficulty_level: int
    player_count: Optional[int] = None
    times: Optional[int] = None
    score: int
    tags: Optional[List[str]] = None

    characters: List[Character]
    content: List[ContentPart]

    class Config:
        from_attributes=True
        
        # 提供一个示例，这将在 FastAPI 文档中显示
        json_schema_extra = {
            "example": {
                "title": "老式公寓谋杀案",
                "description": "一桩发生在密闭公寓内的离奇凶案...",
                "cover_url": "",
                "difficulty_level": 1,
                "score": 60,
                "player_count": 3,
                "times": 60,
                "tags": ["经典", "悬疑", "推理"],
                "characters": [
                    {"name": "嫌疑人 A", "relationship": "同事", "contradictionPoint": "...", "words": "..."},
                    {"name": "嫌疑人 B", "relationship": "邻居", "contradictionPoint": "...", "words": "..."},
                    {"name": "嫌疑人 C", "relationship": "前女友", "contradictionPoint": "...", "words": "..."}
                ],
                "content": [
                    {"type": "text", "text": "老式公寓 302..."},
                    {"type": "clue", "clue_index": 0, "text": "红酒", "clue_text": "...", 
                    "suspect_hints": ["...", "...", "..."]},
                    {
                    "text": "，暗红的酒液正顺着桌角缓缓滴落。死者趴在地板上，背后插着一把",
                    "type": "text"
                    },
                ]
            }
        }

class ScriptResponse(BaseModel):
    uuid: str
    title: str
    description: str
    cover_url: Optional[str]
    difficulty_level: int
    player_count: int
    times: int
    score: int
    tags: List[str]
    created_at: datetime
    # content: List[ContentPart]
    # characters: List[Character]