"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check that all expected activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Tennis Club" in data


def test_get_activities_has_correct_structure(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    data = response.json()
    
    # Pick an activity to validate structure
    activity = data["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_participants_is_list(client):
    """Test that participants field is always a list."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_info in data.items():
        assert isinstance(activity_info["participants"], list), \
            f"{activity_name} participants should be a list"


def test_get_activities_max_participants_is_integer(client):
    """Test that max_participants is an integer."""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_info in data.items():
        assert isinstance(activity_info["max_participants"], int), \
            f"{activity_name} max_participants should be an integer"
