from app.nosql import mongo_db
from app.nosql.model import Request, Response, Book

from typing import List

from app.task.aladin_api import do_request_task


async def find_not_responded_request():
    print("background work start!")
    not_responed_request: List[Request] = await mongo_db.engine.find(
        Request, Request.result_code.match(200)
    )

    print(len(not_responed_request))

    for request in not_responed_request:
        await do_request_task(request.id)
