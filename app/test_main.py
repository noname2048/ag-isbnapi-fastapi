from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    """main 함수를 읽고 루트(/) 응답상태코드가 200인지 확인"""
    response = client.get("/")
    assert response.status_code == 200


def mongo_db_item_exist():
    