from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_employees_by_quarter():
    response = client.get("/analytics/employees_by_quarter")
    assert response.status_code == 200
    assert isinstance(
        response.json(),
        list
    )

def test_departments_above_mean():
    response = client.get("/analytics/departments_above_mean")
    assert response.status_code == 200
    assert isinstance(
        response.json(),
        list
    )

def test_upload_invalid_file():
    response = client.post(
        "/upload/employees",
        files={
            "file":(
                "test.txt",
                b"invalid content",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400

