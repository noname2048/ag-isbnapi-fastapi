from datetime import datetime, timedelta
from typing import Optional

from pathlib import Path
from dotenv import dotenv_values

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi import status

import requests

router = APIRouter()
secret_config = dotenv_values(Path(__file__).parents.parents / ".env")


@router.get("/auth/google/login/redirected", tags=["login", "oauth"])
async def google_auth(code: Optional[str] = Query(None)):
    """구글 로그인 OAuth 리다이렉트를 받는 함수
    ## 1
        프론트에서 구글 로그인 api, "https://accounts.google.com/o/oauth2/v2/auth" 로 안내
        정보는 대략
        clientId: "48231090303-eelp5r7prhev89t13ng9mt8f609pqqhg.apps.googleusercontent.com",
        redirectUri: "http://localhost:8000/auth/api/v1/google/token",
        responseType: "token",
        scope: "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        state: "letslogin",
        loginHint: "sungwook.csw@gmail.com", // optional
    ## 2
        구글 로그인 api가 code를 들고 get으로 현재 함수 실행
    ## 3
        현재 함수에서 code를 access_token으로 바꾸는 작업 수행
        # TODO: signup일 경우 refresh_token DB에 저장하기
        # TODO: login, signup일 경우 access_token을 DB에 저장하기
        # TODO: 요청을 수행할 때마다 access_token 갱신하기
    ## 4
        바꾼 access_token 을 json으로 리턴합니다.
    """
    errors = {"error": "문제가 발생했습니다. code가 존재하지 않습니다."}
    if not code:
        return JSONResponse(
            content=errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    query_dict = {
        "client_id": secret_config["GOOGLE_OAUTH2_CLIENT_ID"],
        "client_secret": secret_config["GOOGLE_OAUTH2_CLIENT_PASSWORD"],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "/auth/api/v1/google/redirected",
    }
    uri = "https://oauth2.googleapis.com/token"

    # access_token으로 바꾸기
    response = requests.post(uri, data=query_dict)
    if response.status_code == 200:
        data = response.json()
        ret = {}
        for k in ["access_token", "expires_in", "scope", "token_type", "refresh_token"]:
            if k in data:
                ret[k] = data[k]
        ret["message"] = "login successfully"
        return ret

    else:
        return {"message": "access token can not gained"}
