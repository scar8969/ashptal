"""Terminal entrypoint."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .chat import ChatSession


def _print_banner() -> None:
    print("=" * 58)
    print("  ASHPTAL — safety-guarded healthcare assistant (Gemini)")
    print("  type 'exit' to quit · 'history' to show session log")
    print("=" * 58)


def _show_history(session: ChatSession) -> None:
    path = session.history_path
    if not path.exists():
        print("(no history yet)")
        return
    print(f"--- {path} ---")
    for line in path.read_text(encoding="utf-8").splitlines():
        print(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ashptal",
        description="Safety-guarded healthcare assistant chatbot (Google Gemini).",
    )
    parser.add_argument("--model", default=None, help="Gemini model name")
    parser.add_argument(
        "--history",
        default=None,
        help="Path to session log (default ~/.ashptal/history.jsonl)",
    )
    parser.add_argument("--version", action="version", version=f"ashptal {__version__}")
    args = parser.parse_args(argv)

    try:
        session = ChatSession(model=args.model) if args.model else ChatSession()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.history:
        session.history_path = args.history

    _print_banner()
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye.")
            return 0
        if user_input.lower() == "history":
            _show_history(session)
            continue

        print("Assistant:", session.ask(user_input))


if __name__ == "__main__":
    sys.exit(main())
