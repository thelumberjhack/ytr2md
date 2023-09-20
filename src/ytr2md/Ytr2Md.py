"""CLI for ytr2md."""
import argparse
import logging
import os
from youtube_transcript_api import YouTubeTranscriptApi

from ytr2md.MdFormatter import MarkDownFormatter


class Ytr2MdCLI:
    """Class for the command line interface of ytr2md.

    Returns:
        None
    """

    @staticmethod
    def parse_args():
        """Parse the command line arguments."""
        parser = argparse.ArgumentParser(
            description='Convert a YouTube video transcript to Markdown.')
        parser.add_argument('video_id', type=str,
                            help='The YouTube video ID.')
        parser.add_argument('-o', '--output', type=str, default="./transcript.md",
                            help='The output file.')
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Verbose output.')
        return parser.parse_args()

    @classmethod
    def main(cls):
        """Main entry point for the ytr2md CLI."""
        args = cls.parse_args()

        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
        )

        video_id = args.video_id
        output = os.path.abspath(args.output)

        logging.info("Fetching transcript for video %s...", video_id)
        tr_list = YouTubeTranscriptApi.list_transcripts(video_id)
        tr = tr_list.find_manually_created_transcript(['en'])
        formatter = MarkDownFormatter()
        tr_md = formatter.format_transcript(tr.fetch(), video_id=video_id)

        with open(output, "w", encoding="utf-8") as out_file:
            out_file.write(tr_md)

        logging.info("Transcript written to %s.", output)
