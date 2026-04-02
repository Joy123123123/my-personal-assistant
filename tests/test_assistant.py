"""Tests for the core Assistant class."""

import pytest
from assistant import Assistant


@pytest.fixture
def assistant():
    return Assistant(name="TestBot")


def test_greet(assistant):
    greeting = assistant.greet()
    assert "TestBot" in greeting
    assert "personal assistant" in greeting.lower()


def test_respond_empty(assistant):
    response = assistant.respond("")
    assert "Please say something" in response


def test_respond_greeting(assistant):
    for phrase in ["hi", "hello", "hey", "Hello!"]:
        response = assistant.respond(phrase)
        assert "hello" in response.lower() or "hi" in response.lower()


def test_respond_farewell(assistant):
    response = assistant.respond("bye")
    assert "goodbye" in response.lower() or "bye" in response.lower()


def test_respond_help(assistant):
    response = assistant.respond("help")
    assert "Calculator" in response
    assert "Notes" in response
    assert "Reminders" in response


def test_respond_time(assistant):
    response = assistant.respond("What time is it?")
    assert response  # non-empty
    assert any(word in response.lower() for word in ["time", "am", "pm"])


def test_respond_date(assistant):
    response = assistant.respond("What is today's date?")
    assert "date" in response.lower() or any(
        month in response
        for month in [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
    )


def test_respond_calculator(assistant):
    response = assistant.respond("calculate 2 + 2")
    assert "4" in response


def test_respond_unknown(assistant):
    response = assistant.respond("xyzzy frobozz")
    assert "help" in response.lower()
