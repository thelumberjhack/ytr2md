import logging
import os
from pathlib import Path

import click
from rich.logging import RichHandler
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
)

from ytr2md.MdFormatter import MarkdownFormatter

# Setting up logging
FORMAT = "%(message)s"
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
    default=os.getcwd(),
    help="Output dir to save the transcripts.",
)
@click.pass_context
def cli(ctx, verbose, output):
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


def fetch_manual_transcript(video_id: str):
    """Fetch manually created English transcript.

    Falls back to `get_transcript` if `list_transcripts` API is unavailable.
    Note: Fallback cannot guarantee the transcript is manually created.
    """
    # Newer API versions expose list_transcripts; older expose instance list().
    if hasattr(YouTubeTranscriptApi, "list_transcripts"):
        tr_list = YouTubeTranscriptApi.list_transcripts(video_id)
        return tr_list.find_manually_created_transcript(["en"])
    # Use instance-based API
    api = YouTubeTranscriptApi()
    tr_list = api.list(video_id)  # type: ignore[attr-defined]
    if hasattr(tr_list, "find_manually_created_transcript"):
        return tr_list.find_manually_created_transcript(["en"])
    return tr_list.find_transcript(["en"])


@cli.command(help="Download and format the transcript of a YouTube video.")
@click.argument("video_id", type=click.STRING)
@click.pass_context
def get(ctx, video_id):  # type: ignore[unused-argument]
    """Download and format the transcript of a YouTube video."""
    output = ctx.obj["output"]
    logger.info(f"Fetching transcript for video '{video_id}'...")
    try:
        tr = fetch_manual_transcript(video_id)
        formatter = MarkdownFormatter()
        tr_md = formatter.format_transcript(tr.fetch(), video_id=video_id)

        with open(
            os.path.join(output, f"{video_id}.md"), "w", encoding="utf-8"
        ) as out_file:
            out_file.write(tr_md)

        logger.info(f"Transcript written to '{output}'.")
        return 0
    except NoTranscriptFound as err:
        logger.debug(err, exc_info=True)
        logger.info("No manually created English transcript found.")
        raise click.exceptions.Exit(1)
    except TranscriptsDisabled as err:
        logger.debug(err, exc_info=True)
        logger.info("Transcripts are disabled for this video.")
        raise click.exceptions.Exit(1)
    except CouldNotRetrieveTranscript as err:
        logger.debug(err, exc_info=True)
        logger.info("Failed to retrieve transcript due to API error.")
        raise click.exceptions.Exit(1)
    except Exception as err:
        logger.debug(err, exc_info=True)
        logger.info(f"Failed to fetch transcript for video '{video_id}'.")
        logger.info("Re-run the command with '-v' for more info.")
        raise click.exceptions.Exit(1)


def main() -> int:
    """Main entry point for the ytr2md CLI."""
    cli()
    return 0
