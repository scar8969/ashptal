"""Tests for the chat session (no live API calls)."""

import json

import pytest

from ashptal.chat import ChatSession


class FakeModel:
    """Stand-in for genai.GenerativeModel — records prompts, returns canned text."""

    def __init__(self, replies=("canned reply",)):
        self.replies = iter(replies)
        self.prompts = []

    def start_chat(self):
        return self

    def send_message(self, prompt):
        self.prompts.append(prompt)
        return type("R", (), {"text": next(self.replies)})()


@pytest.fixture
def session(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr("ashptal.chat.genai.GenerativeModel", FakeModel)
    s = ChatSession(history_path=tmp_path / "history.jsonl")
    s._model = FakeModel()
    s._chat = s._model
    return s


class TestChatSession:
    def test_plain_question_gets_answer(self, session):
        assert session.ask("What is blood pressure?") == "canned reply"

    def test_crisis_never_reaches_model(self, session):
        reply = session.ask("I want to kill myself")
        assert "emergency" in reply.lower()
        assert session._model.prompts == []  # no LLM call

    def test_diagnosis_request_never_reaches_model(self, session):
        session.ask("Do I have cancer?")
        assert session._model.prompts == []

    def test_history_logged(self, session):
        session.ask("What is a fever?")
        lines = session.history_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["question"] == "What is a fever?"
        assert entry["answer"] == "canned reply"
        assert entry["triage"] == "answer"

    def test_crisis_logged_with_triage_tag(self, session):
        session.ask("I want to kill myself")
        entry = json.loads(session.history_path.read_text(encoding="utf-8").splitlines()[0])
        assert entry["triage"] == "crisis"

    def test_missing_key_raises(self, tmp_path, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        with pytest.raises(RuntimeError, match="GEMINI_API_KEY"):
            ChatSession(history_path=tmp_path / "h.jsonl")
