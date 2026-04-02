"""Tests for time commands."""

import pytest
from unittest.mock import patch
from datetime import datetime
from assistant.commands.time_commands import handle_time


_FIXED_DT = datetime(2024, 6, 15, 14, 30, 0)  # Saturday, June 15, 2024, 02:30 PM


@pytest.fixture(autouse=True)
def freeze_time():
    with patch("assistant.commands.time_commands.datetime") as mock_dt:
        mock_dt.now.return_value = _FIXED_DT
        yield mock_dt


def test_handle_time_time():
    response = handle_time("What time is it?")
    assert "02:30 PM" in response


def test_handle_time_date():
    response = handle_time("What is today's date?")
    assert "June 15, 2024" in response


def test_handle_time_day():
    response = handle_time("What day is it?")
    assert "Saturday" in response


def test_handle_time_year():
    response = handle_time("What year is it?")
    assert "2024" in response


def test_handle_time_month():
    response = handle_time("What month is it?")
    assert "June" in response


def test_handle_time_generic():
    response = handle_time("When is it?")
    assert "02:30 PM" in response
    assert "June 15, 2024" in response
