# 剧本杀项目
## 项目简介
本项目是一个基于Python的女友游戏项目。它使用了FastAPI框架，MongoDB作为数据库，Uvicorn作为服务器。

## 项目结构
- `app/`: 包含应用程序的主要代码和配置文件。
  - `main.py`: 应用程序的入口点。
  - `routers/`: 包含路由和API端点的代码。
  - `models/`: 包含数据模型的代码。
  - `schemas/`: 包含数据模型的Pydantic模式。
  - `services/`: 包含业务逻辑的代码。
  - `utils/`: 包含工具函数的代码。
  - `config.py`: 配置文件。
- `scripts/`: 包含脚本的代码。
  - `start.py`: 启动脚本。
- `Dockerfile`: Docker配置文件。
- `README.md`: 项目说明文档。


## 数据库表设计

### 项目模块
1. 用户系统
2. 剧本杀游戏（早期版本，可能废弃）
3. 小游戏系统（含剧本杀、贪吃蛇、俄罗斯方块等）
4. 女友系统

### 模型间的主要关联
1. User与Girl ：一对多关系，用户可以拥有多个女友
2. User与Order ：一对多关系，用户可以有多个订单
3. Girl与GirlTemplate ：一对一关系，每个女友基于一个模板
4. Girl与Goods ：一对多关系，女友可以拥有多种类型的物品
5. Goods与GoodsTemplate ：一对一关系，每个物品基于一个模板
6. User与GameScript ：一对多关系，用户可以有多个剧本杀游戏数据（早期版本，可能废弃）
7. Script与GameScript ：一对多关系，一个剧本可以有多个用户玩游戏（早期版本，可能废弃）
8. User与UserGamePlay ：一对多关系，用户可以有多个小游戏数据
9. User与GameScore ：一对多关系，用户可以有多个小游戏的得分数据


## 启动服务

1. 安装依赖：
```bash
uv sync
```

2. 启动MongoDB服务

3. 创建.env文件并配置环境变量
`cp .env.example .env`

4. 运行应用：
```bash
# 方式1：使用项目提供的启动脚本
uv run python -m scripts.start

# 方式2：直接使用 uvicorn 指定正确的应用路径
uv run uvicorn app.main:app --reload

```

5. docker部署
`docker compose up -d --build`


## API接口文档

启动服务，访问API文档：`http://localhost:8000/docs`


## 开发注意事项
##### 处理缓存文件
```
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```