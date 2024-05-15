import logging
import os
from pathlib import Path

import click
from rich.logging import RichHandler
from youtube_transcript_api import YouTubeTranscriptApi

from ytr2md.MdFormatter import MarkDownFormatter

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


@cli.command(help="Download and format the transcript of a YouTube video.")
@click.argument("video_id", type=click.STRING)
@click.pass_context
def get(ctx, video_id):
    """Download and format the transcript of a YouTube video."""
    output = ctx.obj["output"]
    logger.info(f"Fetching transcript for video '{video_id}'...")
    tr_list = YouTubeTranscriptApi.list_transcripts(video_id)
    try:
        tr = tr_list.find_manually_created_transcript(["en"])
        formatter = MarkDownFormatter()
        tr_md = formatter.format_transcript(tr.fetch(), video_id=video_id)

        with open(
            os.path.join(output, f"{video_id}.md"), "w", encoding="utf-8"
        ) as out_file:
            out_file.write(tr_md)

        logger.info(f"Transcript written to '{output}'.")
    except Exception as err:
        logger.debug(err, exc_info=True)
        logger.info(f"Failed to fetch transcript for video '{video_id}'.")
        logger.info("Re-run the command with '-v' for more info.")


def main() -> int:
    """Main entry point for the ytr2md CLI."""
    cli()
    return 0
