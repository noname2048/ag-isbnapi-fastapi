import logging
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        databse_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)

        self._engine = create_engine(
            databse_url,
            echo=echo,
            pool_recycle=pool_recycle,
        )
