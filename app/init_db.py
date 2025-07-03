import uuid
import logging
from app.models.template import GirlTemplate, GoodsTemplate

logger = logging.getLogger(__name__)

async def init_girl_templates():
    # 检查是否已有模板数据
    templates_count = await GirlTemplate.count()
    if templates_count > 0:
        print("模板数据已存在，跳过初始化")
        return
    
    # 初始化GirlTemplate数据
    girl_templates = [
        GirlTemplate(
            name="小路",
            pic="https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p10.mov",
            age=21,
            height=160,
            job="大学生",
            open_number=0,
            sort=1
        ),
        GirlTemplate(
            name="阿美",
            pic="https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p20.mov",
            age=22,
            height=162,
            job="舞蹈演员",
            open_number=20,
            sort=2
        ),
        GirlTemplate(
            name="小丽",
            pic="https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p30.mov",
            age=18,
            height=168,
            job="cos爱好者",
            open_number=30,
            sort=3
        ),
        GirlTemplate(
            name="阿英",
            pic="https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p40.mov",
            age=25,
            height=164,
            job="古装演员",
            open_number=40,
            sort=4
        )
    ]

    # 插入数据到数据库
    print("初始化女友模版")
    for template in girl_templates:
        await template.insert()
    
    girl_template_1 = await GirlTemplate.find_one(GirlTemplate.name == "小路")
    girl_template_2 = await GirlTemplate.find_one(GirlTemplate.name == "阿美")
    girl_template_3 = await GirlTemplate.find_one(GirlTemplate.name == "小丽")
    girl_template_4 = await GirlTemplate.find_one(GirlTemplate.name == "阿英")
    
    # 初始化GoodsTemplate数据
    goods_templates = [
        # 衣服
        GoodsTemplate(
            name="衣服1",
            pic="https://seo-public.tos-cn-beijing.volces.com/script_kill/clothes_1.jpg",
            goods_type="clothes",
            open_if="gold_coins",
            open_number=0,
        ),
        # 首饰
        GoodsTemplate(
            name="首饰1",
            pic="https://seo-public.tos-cn-beijing.volces.com/script_kill/jewelry_1.jpg",
            goods_type="jewelrys",
            open_if="gold_coins",
            open_number=0,
        ),
        # 其他
        GoodsTemplate(
            name="其他物品1",
            pic="https://seo-public.tos-cn-beijing.volces.com/script_kill/car_1.jpg",
            goods_type="others",
            open_if="gold_coins",
            open_number=0,
        )
    ]
    for template in goods_templates:
        await template.insert()

    dances_templates = []
    # 女友1舞蹈
    for i in range(1, 7):
        coins = 3 if i == 1 else 5
        dances_templates.append(
            GoodsTemplate(
                name=f"舞蹈1-{i}",
                pic=f"https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p1{i}.mov",
                goods_type="dances",
                open_number=coins,
                match_girl_template_id=str(girl_template_1.uuid),
            )
        )
    
    # 女友2舞蹈
    for i in range(1, 2):
        coins = 3 if i == 1 else 5
        dances_templates.append(
            GoodsTemplate(
                name=f"舞蹈2-{i}",
                pic=f"https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p2{i}.mov",
                goods_type="dances",
                open_number=coins,
                match_girl_template_id=str(girl_template_2.uuid),
            )
        )

    # 女友3舞蹈
    for i in range(1, 3):
        coins = 3 if i == 1 else 5
        dances_templates.append(
            GoodsTemplate(
                name=f"舞蹈3-{i}",
                pic=f"https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p3{i}.mov",
                goods_type="dances",
                open_number=coins,
                match_girl_template_id=str(girl_template_3.uuid),
            )
        )
    
    # 女友4舞蹈
    for i in range(1, 3):
        coins = 3 if i == 1 else 5
        dances_templates.append(
            GoodsTemplate(
                name=f"舞蹈4-{i}",
                pic=f"https://seo-ai-images.s3.ap-southeast-1.amazonaws.com/p4{i}.mov",
                goods_type="dances",
                open_number=coins,
                match_girl_template_id=str(girl_template_4.uuid),
            )
        )
    
    # 插入数据到数据库
    print("初始化舞蹈模版")
    for template in dances_templates:
        await template.insert()
    logger.info("模板数据初始化完成")

async def init_game_config():
    from app.models.game import GameType, GameConfig
    # 检查是否已有配置数据
    config_count = await GameConfig.count()
    if config_count > 0:
        print("配置数据已存在，跳过初始化")
        return

    # 初始化配置数据
    game_configs = [
        {
            "name": "剧本杀",
            "game_type": GameType.SCRIPT_KILL,
            "max_plays_per_day": 5,
            "base_score": 10,
            "initial_coins": 100
        },
        {
            "name": "贪吃蛇",
            "game_type": GameType.SNAKE,
            "max_plays_per_day": 10,
            "base_score": 5,
            "initial_coins": 50
        },
        {
            "name": "方块",
            "game_type": GameType.BLOCKS,
            "max_plays_per_day": 10,
            "base_score": 5,
            "initial_coins": 50
        }
    ]

    for config_data in game_configs:
        config = GameConfig(**config_data)
        await config.insert()
        print(f"已创建游戏配置: {config.name}")

async def init_db():
    print("初始化数据库")
    await init_girl_templates()
    await init_game_config()
    print("初始化数据库结束")