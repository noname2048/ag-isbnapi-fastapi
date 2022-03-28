""" 1분마다 작동하는 스케줄러 만들기
1분마다, 100개의 크롤링을 꾸준히 하기 위해 만듦니다.
나중에는 queue에다가 넣어서 배치 프로그램을 돌릴 수 있게 할 예정.
(5000천개 쌓여있으면 100개씩 여러번을 하던지, 여러개의 WAS가 나눠서 풀기)
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from fastapi import FastAPI

from app.utils.logger import mylogger

jobstores = {"default": MongoDBJobStore()}
executors = {"default": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": False, "max_instances": 3}


async def init_scheduler(app: FastAPI):
    async def myjob():
        """몽고DB에서 reuqested, need update 인 Request 객체를 체크
        해당 객체에 대한 response를 만들고 객체 상태를 registered 로 바꾸기

        """
        pass

    @app.on_event("startup")
    async def _init():
        try:
            schedule = AsyncIOScheduler(
                jobstores=jobstores, executors=executors, job_defaults=job_defaults
            )
            schedule.start()
        except:
            mylogger.error("Unable to Create Schedule")
