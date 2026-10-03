"""Safety triage layer — the guardrail between the user and the LLM."""

from __future__ import annotations

import re
from dataclasses import dataclass

# Phrases that signal a request for a diagnosis or prescription.
DIAGNOSIS_PATTERNS = [
    re.compile(r"\b(what|which)\b.{0,40}\b(diagnos|disease|illness|condition)\b", re.I),
    re.compile(r"\b(do i have|is it)\b.{0,40}\b(cancer|diabetes|infection|flu|covid|fever|disease)\b", re.I),
    re.compile(r"\b(prescribe|prescription|medication for|medicine for|drug for|dose of)\b", re.I),
    re.compile(r"\b(should i take|can i take)\b.{0,30}\b(paracetamol|aspirin|ibuprofen|antibiotic|pill|tablet)\b", re.I),
    re.compile(r"\b(how do i treat|how to cure|what cures)\b", re.I),
]

# Crisis keywords — immediate escalation to emergency services.
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "self harm", "self-harm",
    "chest pain", "heart attack", "stroke", "unconscious", "not breathing",
    "severe bleeding", "overdose", "poison",
]

# Topics the assistant will not engage with.
BLOCKED_TOPICS = [
    "illegal drugs", "buy drugs", "sell drugs", "weapon", "bomb",
]


@dataclass(frozen=True)
class TriageResult:
    """Outcome of triaging a user message."""

    action: str  # "answer" | "crisis" | "blocked" | "clarify"
    reason: str = ""


class SafetyTriage:
    """Rule-based guardrail applied before any LLM call."""

    def triage(self, message: str) -> TriageResult:
        text = message.strip()
        if not text:
            return TriageResult("clarify", "empty message")

        lowered = text.lower()

        if any(kw in lowered for kw in CRISIS_KEYWORDS):
            return TriageResult(
                "crisis",
                "This sounds like a medical emergency. Please call your local "
                "emergency number (India: 108 / 112) or go to the nearest "
                "hospital immediately.",
            )

        if any(kw in lowered for kw in BLOCKED_TOPICS):
            return TriageResult("blocked", "I can't help with that topic.")

        if any(p.search(text) for p in DIAGNOSIS_PATTERNS):
            return TriageResult(
                "clarify",
                "I can't diagnose or prescribe — only a doctor can. I can "
                "explain symptoms, treatments, or health concepts in general "
                "terms. Would you like that?",
            )

        return TriageResult("answer")
