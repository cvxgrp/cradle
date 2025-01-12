from unittest.mock import patch

import pytest
import questionary

# Import the module with your functions
# Assuming the original code is in a file called project_setup.py
from cvx.cradle.utils.questions import (
    _validate_description,
    _validate_project_name,
    _validate_status,
    _validate_username,
    ask,
)


def test_validate_project_name_valid():
    valid_names = ["project", "project123", "project_name", "a_very_long_project_name_123"]
    for name in valid_names:
        assert _validate_project_name(name) == name


def test_validate_project_name_invalid():
    invalid_names = [
        "",  # empty
        "Project",  # uppercase
        "123project",  # starts with number
        "project-name",  # invalid character
        "project name",  # space
        "@project",  # special character
    ]
    for name in invalid_names:
        with pytest.raises(ValueError):
            _validate_project_name(name)


def test_validate_username_valid():
    valid_usernames = ["user", "user123", "cvxgrp", "organization-name"]
    for username in valid_usernames:
        assert _validate_username(username) == username


def test_validate_username_invalid():
    invalid_usernames = ["", None]
    for username in invalid_usernames:
        with pytest.raises(ValueError):
            _validate_username(username)


def test_validate_description_valid():
    valid_descriptions = ["A test project", "This is a longer description with multiple words", "Short desc"]
    for desc in valid_descriptions:
        assert _validate_description(desc) == desc


def test_validate_description_invalid():
    invalid_descriptions = ["", None]
    for desc in invalid_descriptions:
        with pytest.raises(ValueError):
            _validate_description(desc)


def test_validate_status_valid():
    valid_statuses = ["public", "private", "internal"]
    for status in valid_statuses:
        assert _validate_status(status) == status


def test_validate_status_invalid():
    invalid_statuses = ["", None, "invalid", "PUBLIC", "Private"]
    for status in invalid_statuses:
        with pytest.raises(ValueError):
            _validate_status(status)


def test_ask_integration():
    # Mock user inputs
    with patch.object(questionary.Question, "ask") as mock_ask:
        # Configure mock to return appropriate values for different questions
        mock_ask.side_effect = [
            "testproject",  # project name
            "testuser",  # username
            "Test description",  # description
            "public",  # status
        ]

        result = ask()

        # Verify the returned context
        assert result["project_name"] == "testproject"
        assert result["username"] == "testuser"
        assert result["description"] == "Test description"
        assert result["status"] == "public"
        assert result["repository_url"] == "https://github.com/testuser/testproject"
        assert result["ssh_uri"] == "git@github.com:testuser/testproject.git"
        assert result["command"] == "gh repo create testuser/testproject --public --description 'Test description'"


def test_ask_with_defaults():
    # Mock user inputs with empty values to test defaults
    with patch.object(questionary.Question, "ask") as mock_ask:
        mock_ask.side_effect = [
            "testproject",  # project name
            "",  # username (should default to "tschm")
            "",  # description (should default to "Some computations")
            "public",  # status
        ]

        result = ask()

        assert result["project_name"] == "testproject"
        assert result["username"] == "tschm"  # default value
        assert result["description"] == "Some computations"  # default value
        assert result["status"] == "public"


# @pytest.fixture
# def mock_questionary():
#     with patch("questionary.text") as mock_text, patch("questionary.select") as mock_select:
#         yield {"text": mock_text, "select": mock_select}
#
#
# def test_ask_error_handling(mock_questionary):
#     # Test that invalid inputs are handled appropriately
#     mock_questionary["text"].return_value.ask.side_effect = ["INVALID_NAME"]
#
#     with pytest.raises(ValueError) as exc_info:
#         ask()
#     assert "Project name must start with a lowercase letter" in str(exc_info.value)