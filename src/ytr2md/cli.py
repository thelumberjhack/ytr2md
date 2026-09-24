import logging
import re
import urllib.parse
from pathlib import Path

import click
from rich.logging import RichHandler
from youtube_transcript_api import (
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    Transcript,
    TranscriptsDisabled,
    YouTubeTranscriptApi,
)

from ytr2md.md_formatter import MarkdownFormatter

# Setting up logging
FORMAT = "%(message)s"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
# URL path forms whose second segment is the video id.
_VIDEO_ID_PATH_PREFIXES = frozenset({"shorts", "embed", "watch", "v", "live"})

logger = logging.getLogger(__name__)


# Setting up the CLI
@click.group()
@click.option(
    "-v", "--verbose", is_flag=True, default=False, help="Enable verbose output."
)
@click.option(
    "-o",
    "--output",
    type=click.Path(exists=True, file_okay=False, writable=True, path_type=Path),
    default=lambda: Path.cwd(),
    help="Output dir to save the transcripts.",
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, output: Path) -> None:
    """Default CLI for ytr2md."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["output"] = output

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])],
    )


def normalize_video_id(raw: str) -> str | None:
    """Extract the canonical video id from common YouTube URL forms.

    Returns the id, or None if the input is not a recognized URL or id.

    Recognized forms: bare ids, `watch?v=<id>` (including schemeless),
    `youtu.be/<id>`, and the `shorts/`, `embed/`, `watch/`, `v/`, and
    `live/` path forms on youtube.com.
    """
    raw = raw.strip()
    if "youtube.com" in raw or "youtu.be" in raw:
        parsed = urllib.parse.urlparse(raw)
        if parsed.netloc.endswith("youtu.be"):
            candidate = parsed.path.strip("/").split("/")[0]
            return candidate or None
        query = urllib.parse.parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]
        parts = [segment for segment in parsed.path.split("/") if segment]
        if len(parts) >= 2 and parts[0] in _VIDEO_ID_PATH_PREFIXES:
            return parts[1]
        return None
    return raw


def fetch_manual_transcript(video_id: str) -> Transcript:
    """Fetch the manually created English transcript for a video.

    Only manually created transcripts are considered; auto-generated
    ones are deliberately rejected.
    """
    api = YouTubeTranscriptApi()
    transcripts = api.list(video_id)
    return transcripts.find_manually_created_transcript(["en"])


@cli.command(help="Download and format the transcript of a YouTube video.")
@click.argument("video_id", type=click.STRING)
@click.pass_context
def get(ctx: click.Context, video_id: str) -> None:
    """Download and format the transcript of a YouTube video."""
    original_input = video_id
    normalized = normalize_video_id(video_id)
    if normalized is None or not VIDEO_ID_RE.fullmatch(normalized):
        logger.info(
            f"'{original_input}' is not a recognizable YouTube video id or URL."
        )
        ctx.exit(1)
    video_id = normalized

    output = Path(ctx.obj["output"]).expanduser().resolve()
    logger.info(f"Fetching transcript for video '{video_id}'...")
    try:
        transcript = fetch_manual_transcript(video_id)
        formatter = MarkdownFormatter()
        tr_md = formatter.format_transcript(transcript.fetch(), video_id=video_id)

        out_file = output / f"{video_id}.md"
        out_file.write_text(tr_md, encoding="utf-8")

        logger.info(f"Transcript written to '{out_file}'.")
        if original_input != video_id:
            logger.info(f"(Extracted video id from input '{original_input}')")
    except NoTranscriptFound as err:
        logger.debug(err, exc_info=True)
        logger.info("No manually created English transcript found.")
        ctx.exit(1)
    except TranscriptsDisabled as err:
        logger.debug(err, exc_info=True)
        logger.info("Transcripts are disabled for this video.")
        ctx.exit(1)
    except CouldNotRetrieveTranscript as err:
        logger.debug(err, exc_info=True)
        logger.info("Failed to retrieve transcript due to API error.")
        ctx.exit(1)
    except Exception as err:
        logger.debug(err, exc_info=True)
        logger.info(f"Failed to fetch transcript for video '{video_id}'.")
        logger.info("Re-run the command with '-v' for more info.")
        ctx.exit(1)


def main() -> int:
    """Main entry point for the ytr2md CLI."""
    cli()
    return 0
