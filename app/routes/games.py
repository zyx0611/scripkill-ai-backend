# routers/scripts.py

from fastapi import APIRouter, Depends
from typing import List

from app.schemas.base_api_response import SuccessResponse
from app.models.game import GameType, GameConfig, UserGamePlay, GameScore, ScoreRequest, ScoreResponseData, GameResponseData
from app.auth import get_current_user
from datetime import date
from app.models.user import User
from app.models.girl import Girl

router = APIRouter()

@router.get(
    "/games",
    response_model=SuccessResponse[List[GameResponseData]],
    summary="小游戏列表"
)
async def get_user_games(current_user: User = Depends(get_current_user)):
    """获取用户的游戏列表"""
    game_configs = await GameConfig.find_all().to_list()
    game_list = []

    for config in game_configs:
        user_game_play = await find_or_create_user_game_play(current_user.uuid, config.game_type)

        plays_today = user_game_play.plays_today
        remaining_plays = max(0, config.max_plays_per_day - plays_today)
        game_list.append(GameResponseData(
            name=config.name,
            type=config.game_type,
            remaining_times=remaining_plays,
            all_times=config.max_plays_per_day,
            base_score=config.base_score
        ))

    return SuccessResponse(data=game_list)


@router.post(
    "/games/score",
    response_model=SuccessResponse[ScoreResponseData],
    summary="小游戏得分提交"
)
async def submit_game_score(score_data: ScoreRequest, current_user: User = Depends(get_current_user)):
    """提交小游戏得分"""
    game_type = score_data.type
    today = date.today()
    girl = await Girl.find_one(Girl.uuid == score_data.girl_id)
    if not girl:
        return SuccessResponse(data=ScoreResponseData(is_ok=False, message="女友不存在", time=0), message="得分提交失败")
    game_config = await GameConfig.find_one(GameConfig.game_type == game_type)
    user_game_play = await find_or_create_user_game_play(current_user.uuid, game_type)

    ## 判断是否重置
    if user_game_play.last_play_time_at.date() != today:
        user_game_play.plays_today = 0
        user_game_play.last_play_time_at = today
    
    ## 判断是否超过次数
    remaining_plays = max(0, game_config.max_plays_per_day - user_game_play.plays_today)
    if remaining_plays == 0:
        return SuccessResponse(data=ScoreResponseData(is_ok=False, message="今日游戏次数已用完", time=0), message="得分提交失败")
    user_game_play.plays_today += 1
    await user_game_play.save()

    ## 保存得分
    game_score = GameScore(
        user_id=current_user.uuid,
        game_type=game_type,
        score=score_data.score,
        girl_id=score_data.girl_id,
        get_exp=score_data.number
    )
    await game_score.insert()

    ## 更新女友经验值
    girl.current_upgrade_value += score_data.number
    if girl.current_upgrade_value >= girl.upgrade_value:
        girl.level += 1
        girl.current_upgrade_value = max(0, girl.current_upgrade_value - girl.upgrade_value)
        girl.upgrade_value = int(girl.upgrade_value * 1.2)
    await girl.save()

    return SuccessResponse(data=ScoreResponseData(is_ok=True, message="得分提交成功", time=remaining_plays - 1), message="得分提交成功")

# 查找或创建 UserGamePlay
async def find_or_create_user_game_play(user_id: str, game_type: GameType):
    today = date.today()
    user_game_play = await UserGamePlay.find_one(UserGamePlay.user_id == user_id, UserGamePlay.game_type == game_type)
    # 如果是该用户第一次玩此游戏类型
    if not user_game_play:
        user_game_play = UserGamePlay(
            user_id=user_id,
            game_type=game_type,
            plays_today=0, # 从0开始
            last_play_time_at=today
        ) 
        await user_game_play.insert()
    return user_game_play