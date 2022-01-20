import logging
from typing import List
from datetime import datetime

from app.nosql.odmantic import mongo_db
from app.nosql.odmantic.model import Request
from app.task.aladin_api import do_request_task
from app.settings.base import REPO_DIR
from app.task.aladin_to_s3 import make_response

logging.basicConfig(
    filename=REPO_DIR / "background.log", encoding="utf-8", level=logging.DEBUG
)


async def check_no_responsed_request_and_make_request():
    """request 모델 중 응답되지 않은 것에 한해서
    response를 생성합니다.
    """
    not_responed_request: List[Request] = await mongo_db.engine.find(
        Request, Request.success.match(None)
    )
    print(
        f"{datetime.strftime(datetime.now(), '%Y-%m-%d')} request 중 response가 없는 {len(not_responed_request)}개의 response를 발견하였습니다."
    )

    for request in not_responed_request:
        response = await make_response(request)
