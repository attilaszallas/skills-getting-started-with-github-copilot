from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_student_from_activity():
    email = "temporary.student@mergington.edu"

    signup_response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/Chess%20Club/participants/{email}")
    assert delete_response.status_code == 200
    assert "Unregistered" in delete_response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess%20Club/participants/missing.student@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
