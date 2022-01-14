from app.nosql import mongo_db
from app.nosql.model import Request
from typing import List
from app.task.aladin_api import do_request_task
import logging
from app.settings.base import REPO_DIR

logging.basicConfig(
    filename=REPO_DIR / "background.log", encoding="utf-8", level=logging.DEBUG
)


async def find_not_responded_request():
    """request 모델 중에서 백그라운드로 처리되지 않고,
    status_code 200으로 남아있는 모델이 있는지 확인하고 백그라운드 태스크를 적용합니다.
    """
    print("background work start!")
    not_responed_request: List[Request] = await mongo_db.engine.find(
        Request, Request.status_code.match(200)
    )

    print(len(not_responed_request))

    for request in not_responed_request:
        await do_request_task(request.id)
