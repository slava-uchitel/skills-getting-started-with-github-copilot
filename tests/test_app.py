from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)

initial_activities = deepcopy(activities)


def setup_function():
    activities.clear()
    activities.update(deepcopy(initial_activities))


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    activity = "Chess Club"
    email = "new_student@mergington.edu"

    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]


def test_duplicate_signup_returns_400():
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity}/signup", params={"email": email}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Already signed up"


def test_unregister_from_activity():
    activity = "Chess Club"
    email = "daniel@mergington.edu"

    response = client.post(
        f"/activities/{activity}/unregister", params={"email": email}
    )
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]


def test_unregister_missing_participant_404():
    activity = "Chess Club"
    email = "not-in-list@mergington.edu"

    response = client.post(
        f"/activities/{activity}/unregister", params={"email": email}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
