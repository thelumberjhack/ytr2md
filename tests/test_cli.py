from pathlib import Path

import pytest
from click.testing import CliRunner

from ytr2md.cli import cli, normalize_video_id


class DummyTranscript:
    def __init__(self, data):
        self._data = data

    def fetch(self):
        return self._data


class DummyTranscriptList:
    def __init__(self, transcript):
        self._transcript = transcript

    def find_manually_created_transcript(self, languages):
        return self._transcript


@pytest.fixture()
def runner():
    return CliRunner()


class DummyApi:
    def __init__(self, transcript_list):
        self._transcript_list = transcript_list

    def list(self, video_id):
        return self._transcript_list


def patch_api(monkeypatch, transcript_list):
    """Patch the module's YouTubeTranscriptApi with a dummy instance-based API."""
    import ytr2md.cli as mod

    monkeypatch.setattr(mod, "YouTubeTranscriptApi", lambda: DummyApi(transcript_list))


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/watch/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/live/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ],
)
def test_normalize_video_id(raw, expected):
    assert normalize_video_id(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "https://www.youtube.com/",
        "https://www.youtube.com/results?search_query=test",
        "https://youtu.be/",
        "https://www.youtube.com/feed/subscriptions",
    ],
)
def test_normalize_video_id_unrecognized(raw):
    assert normalize_video_id(raw) is None


def test_cli_success(monkeypatch, tmp_path: Path, runner: CliRunner):
    sample = [
        {"start": 0.0, "duration": 1.0, "text": "Hello"},
        {"start": 1.0, "duration": 1.2, "text": "World"},
    ]

    patch_api(monkeypatch, DummyTranscriptList(DummyTranscript(sample)))
    video_id = "AbCdEfGhIjk"
    result = runner.invoke(cli, ["-o", str(tmp_path), "get", video_id])
    assert result.exit_code == 0
    out_file = tmp_path / f"{video_id}.md"
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "> Hello" in content and "> World" in content


def test_cli_accepts_full_url(monkeypatch, tmp_path: Path, runner: CliRunner):
    sample = [{"start": 0.0, "duration": 1.0, "text": "Hello"}]

    patch_api(monkeypatch, DummyTranscriptList(DummyTranscript(sample)))
    url = "https://www.youtube.com/watch?v=AbCdEfGhIjk"
    result = runner.invoke(cli, ["-o", str(tmp_path), "get", url])
    assert result.exit_code == 0
    out_file = tmp_path / "AbCdEfGhIjk.md"
    assert out_file.exists()


def test_cli_rejects_unrecognized_input(runner: CliRunner, tmp_path: Path):
    result = runner.invoke(cli, ["-o", str(tmp_path), "get", "not-a-video-id"])
    assert result.exit_code == 1


def test_cli_default_output_is_cwd(monkeypatch, tmp_path: Path, runner: CliRunner):
    sample = [{"start": 0.0, "duration": 1.0, "text": "Hello"}]

    patch_api(monkeypatch, DummyTranscriptList(DummyTranscript(sample)))
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(cli, ["get", "AbCdEfGhIjk"])
    assert result.exit_code == 0
    assert (tmp_path / "AbCdEfGhIjk.md").exists()


def test_cli_no_transcript(monkeypatch, tmp_path: Path, runner: CliRunner):
    from youtube_transcript_api import NoTranscriptFound

    class DummyList:
        def find_manually_created_transcript(self, langs):
            raise NoTranscriptFound("no manual transcript")

    patch_api(monkeypatch, DummyList())
    result = runner.invoke(cli, ["-o", str(tmp_path), "get", "AbCdEfGhIjk"])
    assert result.exit_code == 1
    # no file created
    assert not any(p.name.endswith(".md") for p in tmp_path.iterdir())


def test_cli_transcripts_disabled(monkeypatch, tmp_path: Path, runner: CliRunner):
    from youtube_transcript_api import TranscriptsDisabled

    class DummyList:
        def find_manually_created_transcript(self, langs):
            raise TranscriptsDisabled("disabled")

    patch_api(monkeypatch, DummyList())
    result = runner.invoke(cli, ["-o", str(tmp_path), "get", "AbCdEfGhIjk"])
    assert result.exit_code == 1


def test_cli_api_error(monkeypatch, tmp_path: Path, runner: CliRunner):
    from youtube_transcript_api import CouldNotRetrieveTranscript

    class DummyList:
        def find_manually_created_transcript(self, langs):
            raise CouldNotRetrieveTranscript("api error")

    patch_api(monkeypatch, DummyList())
    result = runner.invoke(cli, ["-o", str(tmp_path), "get", "AbCdEfGhIjk"])
    assert result.exit_code == 1
