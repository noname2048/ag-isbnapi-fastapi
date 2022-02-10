import logging
from multiprocessing import pool
from typing import Callable
from fastapi import FastAPI
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine


class SQLAlchemy:
    def __init__(self):
        self._engine = None
        self._session = None

    def init_sqlalchemy(
        self,
        app: FastAPI,
        dsn: str,
        echo: bool = False,
        **kwargs,
    ) -> None:
        """initiate sqlalchemy connection, bind app with event("startup", "shutdown")

        :param app: fastapi apps
        :param dsn: database source name (url)
        :param echo: echo options of db

        :return: None
        """
        self._engine = create_engine(
            dsn,
            echo=echo,
            # pool_pre_ping=True,  # select 1 before use, auto recycle when it's false
            # pool_recycle=900,  # 15min
        )
        self._session = sessionmaker(
            self._engine,
        )

        @app.on_event("startup")
        def startup():
            self._engine.connect()

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()

    def get_db(self):  # TODO: What is return type
        if self._session is None:
            raise Exception("must be called 'init_sqlalchemy'")
        db_session = self._session()
        try:
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self) -> Callable:
        return self.get_db

    @property
    def engine(self) -> Engine:
        return self._engine


postgresql_db = SQLAlchemy()
Base = declarative_base()
