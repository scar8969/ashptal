# Ashptal — Safety-Guarded Healthcare Assistant

> A terminal-based medical Q&A chatbot powered by Google Gemini. Every question passes through a **safety triage layer** that blocks diagnosis/prescription requests, escalates crisis keywords to emergency services, and enforces a professional-consultation disclaimer.

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Pro-orange)](https://ai.google.dev/)
[![tests](https://img.shields.io/badge/tests-20%20passed-brightgreen)](https://github.com/scar8969/ashptal/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI](https://github.com/scar8969/ashptal/actions/workflows/ci.yml/badge.svg)](https://github.com/scar8969/ashptal/actions/workflows/ci.yml)

## Why this exists

Most "AI health chatbot" repos are a raw `input() → LLM → print()` loop. That's
a demo, not a tool. Ashptal ships the layer those demos skip: a **rule-based
safety triage** that runs *before* the model is ever called.

| What the original never shipped | What Ashptal does |
|---|---|
| Diagnosis/prescription guard | Regex triage blocks "do I have X?", "prescribe me Y" before the LLM |
| Crisis escalation | "chest pain", "kill myself" → immediate emergency-services message, no LLM call |
| Blocked topics | Illegal drugs / weapons refused outright |
| Session history | Every exchange logged to `~/.ashptal/history.jsonl` (JSONL) |
| Error handling | API/network failures return a clear message, not a traceback |
| Test suite | 20 tests — triage rules, session behavior, CLI, no live API needed |
| Installable package | `pip install -e .` → `ashptal` command |

## Quick start

```bash
# 1. Install
pip install -e ".[test]"

# 2. Set your Gemini API key
export GEMINI_API_KEY="your-key"      # macOS/Linux
$env:GEMINI_API_KEY = "your-key"      # Windows PowerShell

# 3. Run
ashptal
```

Type `exit` to quit, `history` to dump the session log.

## How it works

```
You ──▶ SafetyTriage ──▶ answer? ──▶ Gemini 2.5 Pro ──▶ reply
          │  │  │                        │
          │  │  └─ blocked topics ────────┘ (refused)
          │  └─ diagnosis/prescription ────┘ (clarify, no LLM call)
          └─ crisis keywords ───────────────┘ (emergency message)
```

Every exchange is appended to `~/.ashptal/history.jsonl` with a `triage` tag
(`answer` / `clarify` / `crisis` / `blocked`) so you can audit what the bot
refused and why.

## Project structure

```
ashptal/
├── src/ashptal/
│   ├── __init__.py     # public API
│   ├── safety.py       # SafetyTriage — rule-based guardrail
│   ├── chat.py         # ChatSession — triage + Gemini + history
│   └── cli.py          # terminal entrypoint
├── tests/
│   ├── test_safety.py  # triage rules (parametrized)
│   ├── test_chat.py    # session behavior, no live API
│   └── test_cli.py     # CLI flags + error paths
├── pyproject.toml      # installable package, `ashptal` command
└── .github/workflows/ci.yml  # pytest on 3.10/3.11/3.12
```

## Using it as a library

```python
from ashptal import ChatSession

session = ChatSession()          # reads GEMINI_API_KEY from env
print(session.ask("What is blood pressure?"))
```

## License

MIT
