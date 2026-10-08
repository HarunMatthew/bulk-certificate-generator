from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop",
            "date": "2026-10-08",
            "recipients": [
                {"name": "Test User", "email": "test@example.com"},
                {"name": "Another User", "email": "another@example.com"},
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["successful"] == 2
    assert data["failed"] == 0
    assert data["status"] == "COMPLETED"


def test_invalid_email():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop",
            "date": "2026-10-08",
            "recipients": [{"name": "Test User", "email": "invalid-email"}],
        },
    )

    assert response.status_code == 422


def test_get_job():
    response = client.get("/api/jobs/1")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == 1
    assert "status" in data
    assert "total" in data


def test_get_certificates():
    response = client.get("/api/jobs/1/certificates/")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == 1
    assert "certificates" in data


def test_download_certificate():
    response = client.get("/api/certificates/1")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
