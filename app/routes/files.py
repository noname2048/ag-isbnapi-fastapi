import pandas as pd
from fastapi import FastAPI, File, UploadFile, APIRouter
from io import StringIO

router = APIRouter()


@router.post("/files/")
async def upload_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    print(df.text)
    return {"msg": f"{df.text}"}
