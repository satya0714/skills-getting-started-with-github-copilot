"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_successful(client):
    """Test successful signup for an activity."""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    new_email = "student123@mergington.edu"
    
    # Signup
    response = client.post(
        f"/activities/Programming Class/signup?email={new_email}"
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities = client.get("/activities").json()
    participants = activities["Programming Class"]["participants"]
    assert new_email in participants


def test_signup_with_nonexistent_activity(client):
    """Test signup fails for a non-existent activity."""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_registration_fails(client):
    """Test that a student cannot register twice for the same activity."""
    email = "duplicate@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/Drama Club/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        f"/activities/Drama Club/signup?email={email}"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "Already signed up" in data["detail"]


def test_signup_with_valid_email_format(client):
    """Test signup with various email formats."""
    valid_emails = [
        "user@mergington.edu",
        "firstname.lastname@mergington.edu",
        "user+tag@mergington.edu",
    ]
    
    for email in valid_emails:
        response = client.post(
            f"/activities/Art Studio/signup?email={email}"
        )
        assert response.status_code == 200


def test_signup_returns_confirmation_message(client):
    """Test that signup returns an appropriate confirmation message."""
    response = client.post(
        "/activities/Robotics Club/signup?email=robot@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up robot@mergington.edu for Robotics Club"
