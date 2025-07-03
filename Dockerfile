# 使用Python 3.13作为基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# 安装uv
RUN pip install --no-cache-dir uv

# 复制项目文件
COPY . /app/

# 使用uv安装依赖
RUN uv pip install --system -e .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uv", "run", "python", "-m", "scripts.start"]