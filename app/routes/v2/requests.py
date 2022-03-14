from typing import IO, List, Optional
from datetime import datetime
import shutil
from tempfile import NamedTemporaryFile
import csv
import re
from numpy import kaiser

from starlette import status

from fastapi import APIRouter, Body, File, UploadFile, Header, Depends, HTTPException

from pydantic import BaseModel, Field

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request
from app.exceptions import request_error

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
        raise request_error.RequestExsist()

    now = datetime.utcnow()
    new_request = Request(isbn=isbn, created_at=now, updated_at=now, status="requested")
    request = await engine.save(Request)
    return request


class SingleRequestForm(BaseModel):
    isbn: str = Field(..., regex=r"^\d{13}$")
    update: Optional[bool] = False


isbn_pattern = re.compile(r"^\d{13}$")


@router.post("/requests/multi")
async def bulk_request_with_q(qs: List[str]):
    engine = singleton_mongodb.engine

    requests = []
    for q in qs:
        if isbn_pattern.match(q):
            request = await engine.find(Request, {"isbn": q})
            if not request:
                current_time = datetime.utcnow()
                new_request = Request(
                    isbn=q,
                    created_at=current_time,
                    updated_at=current_time,
                    status="requested",
                )
                request = await engine.save(new_request)
                requests += [request]

    return {"accepted": len(requests), "requests": requests}


@router.post("/requests/json")
async def bulk_request(requests_form: List[SingleRequestForm] = Body(...)):
    engine = singleton_mongodb.engine

    requests = []
    if not requests_form:
        return requests

    for request_form in requests_form:
        request = await engine.find(Request, {"isbn": request_form.isbn})
        if request and request_form.update:
            request.status = "need update"
            await engine.save(request)
            continue

        if request:
            continue

        now = datetime.utcnow()
        new_request = Request(
            isbn=request_form.isbn, created_at=now, updated_at=now, status="requested"
        )
        request = await engine.save(Request)
        requests += [request]

    return {"result": len(requests), "requests": requests}


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
            raise request_error.RequeustFileTooBig()

        temp.write(chunk)
    temp.close()

    engine = singleton_mongodb.engine

    requests = []
    with open(temp.name) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            for col in row:
                if isbn_pattern.match(col):
                    request = await engine.find_one({"isbn": col})
                    if not request:
                        current_time = datetime.utcnow()
                        new_request = Request(
                            isbn=col,
                            created_at=current_time,
                            updated_at=current_time,
                            status="requested",
                        )
                        request = await engine.save(new_request)
                        requests += [request]

    return {"accepted": len(requests), "requests": requests}

    # shutil.move(temp.name, )
