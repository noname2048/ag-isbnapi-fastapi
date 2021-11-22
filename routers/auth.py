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


@router.post("/auth/google/login/redirected")
async def signup(code: Optional[str] = Query(None)):
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
