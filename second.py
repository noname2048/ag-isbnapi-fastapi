from typing import Optional, List
import datetime

from fastapi import (
    FastAPI,
    Path,
    Query,
    Body,
    Cookie,
    Header,
    Form,
    File,
    UploadFile,
    Request,
    status,
)
from fastapi.responses import Response, FileResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, Field
from pydantic.errors import JsonTypeError
from second_util import query_and_register

from dotenv import dotenv_values
import pathlib
import aiohttp
import requests

REPO_DIR = pathlib.Path(__file__).parent
secret_config = dotenv_values(REPO_DIR / ".env")

app = FastAPI(
    title="ag-isbnapi-fastapi", description="isbn을 저장하는 마이크로서비스", version="0.0.1"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter
@app.get("/isbn/{isbn}")
async def search_isbn(
    isbn: str = Path(
        ..., title="book isbn, length will be 13", min_length=13, max_length=13
    )
):
    return {"isbn": isbn}


# query parameter
@app.get("/search")
async def search(
    isbn: Optional[str] = Query(
        None,
        title="isbn 넘버",
        description="책을 isbn으로 검색합니다. 13자리 isbn을 사용합니다.",
        min_legnth=13,
        max_length=13,
    ),
    title: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="title search(option)",
        description="제목으로 검색합니다. 단, 한글자는 필요합니다.",
    ),
):
    result = {"result": "not implemented"}
    return result


# meet pydantic
class RequestBookInfo(BaseModel):
    isbn: str = Field(..., regex=r"^[0-9]{13}$", example="9788966261840")
    title: Optional[str] = Field(None, example="Two Scopoops of Django")
    date: datetime.datetime = Field(None, example=datetime.datetime.now())


class ResponseBookInfo(BaseModel):
    isbn: str = Field(..., example="9788966261840")
    title: str = Field(..., example="Two Scopoops of Django")


# @app.get("/request", response_model=ResponseBookInfo)
@app.get("/request")
async def request_book(
    isbn: List[str] = Query(..., regex="^[0-9]{13}$", example="9788966261840")
):
    """한개의 isbn 혹은 여러개의 isbn을 get, query로 받습니다
    받은 isbn은 개인 DB에 없으면 알라딘API를 이용해 정보를 등록합니다.
    """
    response = {}
    for i in isbn:
        book, status = await query_and_register(i)
        response[i] = [book["title"], status]

    return response


#
@app.post("/request")
async def request_book(
    book: List[RequestBookInfo] = Body(..., example={"isbn": "9788966261840"})
):
    """처리할 isbn정보를 post로 받는 함수
    받은 isbn은 개인 DB에 없으면 알라딘API를 이용해 정보를 등록합니다.
    # TODO: 어떻게 여러개의 isbn을 받을 것인지 연구
    """
    book.date = datetime.datetime.now()
    return book


@app.post("/login/")
async def login(email: str = Form(...), password: str = Form(...)):
    """유저로그인을 위한 함수
    email과 password를 받아 처리한다
    """
    return {"email": email}


@app.get("/auth/api/v1/google/login")
async def google_login_start(request: Request):
    """구글 로그인 버튼을 보여주는 페이지"""
    return templates.TemplateResponse("google_login_button.html", {"request": request})


@app.get("/auth/api/v1/google/script.js")
async def google_login_script():
    return FileResponse("templates/script.js")


@app.get("/auth/api/v1/google/redirected")
async def google_login_redirected(access_token: str):
    """구글 로그인 이후 리다이렉트 되는 페이지"""
    return {"message": "hello"}


def google_uri():
    info = {
        "client_id": secret_config["GOOGLE_OAUTH2_CLIENT_ID"],
        "redirect_uri": "http://localhost:8000/auth/api/v1/google/server/redirected",
        "response_type": "code",
        "scope": " ".join(
            [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ]
        ),
        "access_type": "online",
        "state": "login_wep_app",
        "prompt": "select_account",
    }
    uri = "https://accounts.google.com/o/oauth2/v2/auth"
    query_param = "&".join([f"{k}={v}" for k, v in info.items()])

    uri = f"{uri}?{query_param}"
    return uri


@app.get("/auth/api/v1/google/server/login")
async def google_login_redirect():
    # return {"message": google_uri()}
    return RedirectResponse(google_uri())


async def google_code_to_access_token(code: str):
    uri = "https://oauth2.googleapis.com/token"
    info = {
        "client_id": secret_config["GOOGLE_OAUTH2_CLIENT_ID"],
        "client_secret": secret_config["GOOGLE_OAUTH2_CLIENT_PASSWORD"],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/auth/api/v1/google/server/token",
    }

    r = requests.post("https://oauth2.googleapis.com/token", data=info)
    return {
        "status_code": r.status_code,
        "request_uri": r.request.url,
        "request_params": r.request.body,
    }
    if r.status_code == status.HTTP_200_OK:
        return r.status_code
        data = r.json()
        core_data = {
            "access_token": data["access_token"],
            "expires_in": data["expires_in"],
            "refresh_token": data["refresh_token"],
            "scope": data["scope"],
            "token_type": data["token_type"],
        }
        return core_data
    else:
        return JsonTypeError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "로그인에 문제가 있습니다. 서버관리자에게 연락하세요"},
        )


@app.get("/auth/api/v1/google/server/redirected")
async def google_login_redirected(
    state: str, code: str, scope: str, authuser: str, prompt: str
):
    temp = await google_code_to_access_token(code)
    return {
        "state": state,
        "code": code,
        "scope": scope,
        "authuser": authuser,
        "prompt": prompt,
        "uri": temp,
    }


@app.get("/auth/api/v1/google/server/token")
async def google_login_token(
    access_token, expires_in, refresh_token, scope, token_type
):
    return {
        "access_token": access_token,
        "expires_in": expires_in,
        "refresh_token": refresh_token,
        "scope": scope,
        "token_type": token_type,
    }
