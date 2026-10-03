"""Tests for the CLI (no live API calls)."""

from ashptal import cli


def test_version_flag(capsys):
    with pytest_raises_system_exit():
        cli.main(["--version"])
    out = capsys.readouterr().out
    assert "ashptal" in out


def test_missing_key_returns_2(capsys, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert cli.main([]) == 2
    assert "GEMINI_API_KEY" in capsys.readouterr().err


def pytest_raises_system_exit():
    import contextlib

    @contextlib.contextmanager
    def _cm():
        try:
            yield
        except SystemExit:
            pass
    return _cm()
