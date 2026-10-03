"""Ashptal — safety-guarded healthcare assistant chatbot.

A terminal-based medical Q&A chatbot built on Google Gemini. Every question
passes through a safety triage layer that blocks diagnosis/prescription
requests, detects crisis keywords, and enforces a professional-consultation
disclaimer — so the assistant stays helpful without overstepping into
clinical advice.
"""

__version__ = "1.0.0"

from .safety import SafetyTriage, TriageResult
from .chat import ChatSession

__all__ = ["SafetyTriage", "TriageResult", "ChatSession", "__version__"]
