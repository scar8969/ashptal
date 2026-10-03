"""Chat session — wraps the Gemini model with triage + history."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import google.generativeai as genai

from .safety import SafetyTriage

SYSTEM_PROMPT = (
    "You are a professional medical assistant. "
    "Provide concise, factual answers in the same language as the user's question. "
    "Do NOT provide diagnoses or prescriptions. "
    "Advise users to consult healthcare professionals for medical concerns."
)

DEFAULT_MODEL = "models/gemini-2.5-pro-preview-05-06"


class ChatSession:
    """A single chat conversation with triage, history, and logging."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        history_path: str | Path | None = None,
    ) -> None:
        self.triage = SafetyTriage()
        self.model_name = model
        self.history_path = (
            Path(history_path)
            if history_path
            else Path.home() / ".ashptal" / "history.jsonl"
        )
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

        key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY not set. Run: export GEMINI_API_KEY=your-key"
            )
        genai.configure(api_key=key)
        self._model = genai.GenerativeModel(model)
        self._chat = self._model.start_chat()

    def ask(self, message: str) -> str:
        """Triage a message, then answer. Returns the assistant reply."""
        result = self.triage.triage(message)
        if result.action != "answer":
            self._log(message, result.reason, triage=result.action)
            return result.reason

        prompt = f"{SYSTEM_PROMPT}\nQuestion: {message}\nAnswer:"
        try:
            response = self._chat.send_message(prompt)
            reply = response.text.strip()
        except Exception as exc:  # network / API errors
            reply = (
                "Sorry, I couldn't reach the model. Please check your API key "
                f"and connection. ({exc.__class__.__name__})"
            )
        self._log(message, reply)
        return reply

    def _log(self, question: str, answer: str, triage: str = "answer") -> None:
        entry = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "triage": triage,
            "question": question,
            "answer": answer,
        }
        with self.history_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
