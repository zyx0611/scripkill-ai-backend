## 游戏模型设计

## 1. GameConfig 配置游戏全局数据，包括游戏的总轮数、每个玩家的初始金币等。
## 2. UserGamePlay 用户的游戏数据，包括游戏当日次数等。
## 3. GameScore 记录每次用户的游戏得分情况信息

from .base import BaseDocument
from pydantic import Field
from datetime import datetime
from enum import Enum
import pymongo
from pymongo import IndexModel
from pydantic import BaseModel


class GameType(Enum):
    SCRIPT_KILL = 1 # 剧本杀
    SNAKE = 2       # 贪吃蛇
    BLOCKS = 3      # 方块

# --- 游戏请求响应模型 ---
class ScoreRequest(BaseModel):
    type: GameType = Field(..., description="游戏类型")
    score: int = Field(..., ge=0, description="游戏得分")
    girl_id: str = Field(..., description="女友ID")
    number: int = Field(..., description="经验值")

class ScoreResponseData(BaseModel):
    is_ok: bool = Field(..., description="是否成功保存积分")
    message: str = Field(..., description="数据无效（如：用户次数不足）")
    time: int = Field(None, description="剩余可玩次数")

class GameResponseData(BaseModel):
    name: str = Field(..., description="游戏名称，如剧本杀、贪吃蛇")
    type: GameType = Field(..., description="游戏类型，1剧本杀；2贪吃蛇；3方块")
    remaining_times: int = Field(..., description="当前游戏可玩的总次数（每日最大限制）")
    all_times: int = Field(..., description="当前游戏今日剩余可玩次数")
    base_score: int = Field(..., description="基础得分")


# --- 游戏存储模型 ---
class GameConfig(BaseDocument):
    """游戏配置"""
    name: str = Field(..., description="游戏名称")
    game_type: GameType = Field(..., description="游戏类型", unique=True)
    base_score: int = Field(..., description="基础得分")
    max_plays_per_day: int = Field(..., description="每日最大游戏次数")
    initial_coins: int = Field(..., description="初始金币数量")
    class Settings:
        name = "game_configs"

class UserGamePlay(BaseDocument):
    """用户游戏数据"""
    user_id: str = Field(..., description="用户ID")
    game_type: GameType = Field(..., description="游戏类型")
    plays_today: int = Field(..., description="今日游戏次数")
    last_play_time_at: datetime = Field(..., description="上次游戏时间") ## 判断是否重置

    class Settings:
        name = "user_game_plays"
        indexes = [
            IndexModel([("user_id", pymongo.ASCENDING), ("game_type", pymongo.ASCENDING)], unique=True),
        ]

class GameScore(BaseDocument):
    """游戏得分记录"""
    user_id: str = Field(..., description="用户ID")
    game_type: GameType = Field(..., description="游戏类型")
    score: int = Field(..., description="得分")
    girl_id: str = Field(..., description="女友ID")
    get_exp: datetime = Field(..., description="获得女友经验值")
    class Settings:
        name = "game_scores"
        indexes = [
            IndexModel([("user_id", pymongo.ASCENDING), ("game_type", pymongo.ASCENDING), ("score", pymongo.DESCENDING)]),
        ]
