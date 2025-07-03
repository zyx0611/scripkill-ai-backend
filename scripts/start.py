#!/usr/bin/env python3
"""
应用启动脚本
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import uvicorn
from app.config import settings


def main():
    """启动应用"""
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=True,
        use_colors=True,
    )


if __name__ == "__main__":
    main()
