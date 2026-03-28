"""Tests for the DELETE /activities/{activity_name}/participant endpoint."""

import pytest


def test_remove_participant_successful(client):
    """Test successful removal of a participant from an activity."""
    # First, get an existing participant
    activities = client.get("/activities").json()
    chess_participants = activities["Chess Club"]["participants"]
    email_to_remove = chess_participants[0]
    
    # Remove the participant
    response = client.delete(
        f"/activities/Chess Club/participant?email={email_to_remove}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email_to_remove in data["message"]


def test_remove_participant_actually_removes(client):
    """Test that deletion actually removes the participant."""
    email = "michael@mergington.edu"
    
    # Verify participant exists before deletion
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    
    # Delete the participant
    response = client.delete(
        f"/activities/Chess Club/participant?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant is removed
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_remove_from_nonexistent_activity(client):
    """Test removal fails for a non-existent activity."""
    response = client.delete(
        "/activities/Fake Club/participant?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_remove_nonexistent_participant(client):
    """Test removal fails when participant is not registered."""
    response = client.delete(
        "/activities/Chess Club/participant?email=nonexistent@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Participant not found" in data["detail"]


def test_remove_participant_decreases_participant_count(client):
    """Test that removal decreases the participant count."""
    # Get initial count
    activities = client.get("/activities").json()
    initial_count = len(activities["Programming Class"]["participants"])
    
    # Remove a participant
    email = activities["Programming Class"]["participants"][0]
    client.delete(f"/activities/Programming Class/participant?email={email}")
    
    # Check new count
    activities = client.get("/activities").json()
    new_count = len(activities["Programming Class"]["participants"])
    
    assert new_count == initial_count - 1


def test_remove_participant_multiple_times(client):
    """Test removing multiple different participants."""
    activities = client.get("/activities").json()
    initial_participants = activities["Tennis Club"]["participants"].copy()
    
    # Remove first participant
    if len(initial_participants) > 0:
        email1 = initial_participants[0]
        response1 = client.delete(
            f"/activities/Tennis Club/participant?email={email1}"
        )
        assert response1.status_code == 200
    
    # Remove second participant (if exists)
    if len(initial_participants) > 1:
        email2 = initial_participants[1]
        response2 = client.delete(
            f"/activities/Tennis Club/participant?email={email2}"
        )
        assert response2.status_code == 200
        
        # Verify both are removed
        activities = client.get("/activities").json()
        assert email1 not in activities["Tennis Club"]["participants"]
        assert email2 not in activities["Tennis Club"]["participants"]
