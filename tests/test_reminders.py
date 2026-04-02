"""Tests for reminders command."""

import json
import pytest
from assistant.commands.reminders import (
    add_reminder,
    list_reminders,
    complete_reminder,
    delete_reminder,
    handle_reminders,
)


@pytest.fixture
def store(tmp_path):
    return str(tmp_path / "reminders.json")


class TestAddReminder:
    def test_add_reminder_returns_confirmation(self, store):
        response = add_reminder("Call the dentist", store)
        assert "Call the dentist" in response
        assert "#1" in response

    def test_add_multiple_reminders_increments_id(self, store):
        add_reminder("First", store)
        response = add_reminder("Second", store)
        assert "#2" in response

    def test_reminder_persisted(self, store):
        add_reminder("Persisted", store)
        with open(store) as fh:
            reminders = json.load(fh)
        assert reminders[0]["content"] == "Persisted"
        assert reminders[0]["done"] is False


class TestListReminders:
    def test_list_empty(self, store):
        response = list_reminders(store)
        assert "no pending" in response.lower()

    def test_list_shows_pending(self, store):
        add_reminder("Alpha task", store)
        add_reminder("Beta task", store)
        response = list_reminders(store)
        assert "Alpha task" in response
        assert "Beta task" in response

    def test_done_reminders_not_listed(self, store):
        add_reminder("Done task", store)
        complete_reminder(1, store)
        response = list_reminders(store)
        assert "Done task" not in response


class TestCompleteReminder:
    def test_complete_existing(self, store):
        add_reminder("Finish report", store)
        response = complete_reminder(1, store)
        assert "done" in response.lower()

    def test_complete_nonexistent(self, store):
        response = complete_reminder(99, store)
        assert "not found" in response.lower()


class TestDeleteReminder:
    def test_delete_existing(self, store):
        add_reminder("To delete", store)
        response = delete_reminder(1, store)
        assert "deleted" in response.lower()

    def test_delete_nonexistent(self, store):
        response = delete_reminder(99, store)
        assert "not found" in response.lower()


class TestHandleReminders:
    def test_add_via_handle(self, store):
        response = handle_reminders("remind me to buy groceries", store)
        assert "buy groceries" in response.lower()

    def test_list_via_handle(self, store):
        add_reminder("Test reminder", store)
        response = handle_reminders("list reminders", store)
        assert "Test reminder" in response

    def test_done_via_handle(self, store):
        add_reminder("Finish work", store)
        response = handle_reminders("done #1", store)
        assert "done" in response.lower()

    def test_delete_via_handle(self, store):
        add_reminder("Delete me", store)
        response = handle_reminders("delete reminder #1", store)
        assert "deleted" in response.lower()

    def test_unknown_reminder_query(self, store):
        response = handle_reminders("something weird", store)
        assert "remind" in response.lower()
