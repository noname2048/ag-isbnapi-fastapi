from fastapi import APIRouter, WebSocket, Path
from app.nosql import mongo_db
from app.nosql.model import Request

router = APIRouter()


@router.websocket("/ws/requests/{id}")
async def websocket_endpoint(websocket: WebSocket, id: str = Path(...)):
    await websocket.accept()
    r: Request = mongo_db.engine.find_one(Request, Request.id.match(id))
    if r:
        {"success": "wait for code"}
        if r.result_code == 200:
            while True:
            await websocket.send_jso})
        else:
            await websocket.send_json({"done": "already have response"})
    else:
        await websocket.send_json({"error": "not valid request id"})
