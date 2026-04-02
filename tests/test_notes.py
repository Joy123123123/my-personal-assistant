"""Tests for notes command."""

import os
import json
import pytest
import tempfile
from assistant.commands.notes import (
    add_note,
    list_notes,
    delete_note,
    handle_notes,
)


@pytest.fixture
def store(tmp_path):
    return str(tmp_path / "notes.json")


class TestAddNote:
    def test_add_note_returns_confirmation(self, store):
        response = add_note("Buy milk", store)
        assert "Buy milk" in response
        assert "#1" in response

    def test_add_multiple_notes_increments_id(self, store):
        add_note("First", store)
        response = add_note("Second", store)
        assert "#2" in response

    def test_note_persisted(self, store):
        add_note("Persisted note", store)
        with open(store) as fh:
            notes = json.load(fh)
        assert notes[0]["content"] == "Persisted note"


class TestListNotes:
    def test_list_empty(self, store):
        response = list_notes(store)
        assert "no notes" in response.lower()

    def test_list_shows_notes(self, store):
        add_note("Alpha", store)
        add_note("Beta", store)
        response = list_notes(store)
        assert "Alpha" in response
        assert "Beta" in response


class TestDeleteNote:
    def test_delete_existing(self, store):
        add_note("To delete", store)
        response = delete_note(1, store)
        assert "deleted" in response.lower()

    def test_delete_nonexistent(self, store):
        response = delete_note(99, store)
        assert "not found" in response.lower()

    def test_note_removed_after_delete(self, store):
        add_note("Gone", store)
        delete_note(1, store)
        response = list_notes(store)
        assert "no notes" in response.lower()


class TestHandleNotes:
    def test_add_via_handle(self, store):
        response = handle_notes("add note: Remember to call Alice", store)
        assert "Remember to call Alice" in response

    def test_list_via_handle(self, store):
        add_note("Test note", store)
        response = handle_notes("list notes", store)
        assert "Test note" in response

    def test_delete_via_handle(self, store):
        add_note("Delete me", store)
        response = handle_notes("delete note #1", store)
        assert "deleted" in response.lower()

    def test_unknown_notes_query(self, store):
        response = handle_notes("note something weird", store)
        assert "add note" in response.lower() or "list" in response.lower()
