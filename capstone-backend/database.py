import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 在 Render 等云端，把 USE_SQLITE 设置为 "true"，
# 本地 / Docker 不设置（默认 false），仍然用 MySQL。
USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

if USE_SQLITE:
    # 云端：用 SQLite，文件名 app.db，保存在工作目录
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
    connect_args = {"check_same_thread": False}
else:
    # 本地 / Docker：用 MySQL，配合 docker-compose 的 db 容器
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
    DB_NAME = os.getenv("DB_NAME", "news_posts")

    SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connect_args,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
