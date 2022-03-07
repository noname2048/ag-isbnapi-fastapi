from typing import IO, List
from datetime import datetime
import shutil
from tempfile import NamedTemporaryFile
import csv

from starlette import status

from fastapi import APIRouter, Body, File, UploadFile, Header, Depends, HTTPException

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request

router = APIRouter()


@router.get("/requests")
async def list_requests():
    """"""
    engine = singleton_mongodb.engine
    requests = await engine.find(Request, {}, limit=100)
    if requests:
        return requests
    return []


@router.post("/requests")
async def make_request(
    isbn: str = Body(..., regex=r"^\d{13}$"), update: bool = Body(False)
):
    """"""
    engine = singleton_mongodb.engine
    request = await engine.find(Request, {"isbn": isbn})
    if request and update:
        request.status = "need update"
        await engine.save(request)
        return request

    if request:
        raise Exception("already requested")

    now = datetime.utcnow()
    new_request = Request(isbn=isbn, created_at=now, updated_at=now, status="requested")
    request = await engine.save(Request)
    return request


@router.post("/requests/list")
async def bulk_request(isbns: List[int] = Body(...)):
    pass


@router.post("requests/csv")
async def csv_request(
    file: UploadFile = File(
        ...,
        description="csv file with form data",
    )
):
    file_size_limit = 80_000
    real_file_size = 0

    temp: IO = NamedTemporaryFile(delete=False)
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > file_size_limit:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Too large"
            )
        temp.write(chunk)
    temp.close()

    with open(temp.name) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            pass
    # shutil.move(temp.name, )
