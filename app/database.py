from motor.motor_asyncio import AsyncIOMotorClient
import logging
from app.config import settings
from beanie import init_beanie
from app.models.user import User, Order
from app.models.script import Script, GameScript
from app.models.girl import Girl, Goods
from app.models.template import GirlTemplate, GoodsTemplate
from app.models.game import GameConfig, UserGamePlay, GameScore

logger = logging.getLogger(__name__)

# 所有文档模型列表
DOCUMENT_MODELS = [
    User,
    Girl,
    Goods,
    GirlTemplate,
    GoodsTemplate,
    Script,
    GameScript,
    GameConfig,
    UserGamePlay,
    GameScore,
    Order
]


async def connect_to_mongo() -> None:
    """连接MongoDB并初始化Beanie"""
    try:
        logger.info(f"连接MongoDB: {settings.mongodb_url}")
        client = AsyncIOMotorClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
        )
        
        # 测试连接
        await client.admin.command("ismaster")
        logger.info("成功连接到MongoDB")
        
        # 初始化Beanie
        await init_beanie(
            database=client[settings.database_name],
            document_models=DOCUMENT_MODELS
        )
        
        logger.info("Beanie初始化完成")
        
        return client
    except Exception as e:
        logger.error(f"MongoDB连接失败: {e}")
        raise


async def close_mongo_connection(client) -> None:
    """关闭MongoDB连接"""
    if client:
        client.close()
        logger.info("已断开MongoDB连接")
