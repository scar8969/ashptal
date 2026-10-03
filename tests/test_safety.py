"""Tests for the safety triage layer."""

import pytest

from ashptal.safety import SafetyTriage


@pytest.fixture
def triage():
    return SafetyTriage()


class TestTriage:
    def test_plain_question_answered(self, triage):
        assert triage.triage("What is the normal body temperature?").action == "answer"

    def test_foreign_language_answered(self, triage):
        assert triage.triage("¿Qué es la presión arterial?").action == "answer"

    def test_empty_message_clarified(self, triage):
        assert triage.triage("   ").action == "clarify"

    def test_crisis_keyword_escalates(self, triage):
        assert triage.triage("I want to kill myself").action == "crisis"

    def test_chest_pain_escalates(self, triage):
        assert triage.triage("I have chest pain right now").action == "crisis"

    @pytest.mark.parametrize(
        "msg",
        [
            "Do I have cancer?",
            "What disease do I have?",
            "Can you prescribe antibiotics for me?",
            "Should I take paracetamol?",
            "How do I treat this infection?",
        ],
    )
    def test_diagnosis_requests_clarified(self, triage, msg):
        assert triage.triage(msg).action == "clarify"

    def test_blocked_topic(self, triage):
        assert triage.triage("Where can I buy illegal drugs?").action == "blocked"

    def test_crisis_reason_mentions_emergency(self, triage):
        reason = triage.triage("I want to kill myself").reason
        assert "emergency" in reason.lower()
