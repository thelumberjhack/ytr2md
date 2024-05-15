"""Module providing a Markdown formatter for the youtube_transcript_api."""

from youtube_transcript_api.formatters import Formatter


class MarkDownFormatter(Formatter):
    """Markdown formatter for the youtube_transcript_api."""

    @staticmethod
    def format_timestamp(start: str) -> str:
        """Format the start timestamp to HH:mm:ss.

        Args:
            start (string): the start timestamp in seconds

        Returns:
            string: the timestamp formatted as HH:mm:ss
        """
        start_time = float(start)
        hours = int(start_time // 3600)
        minutes = int((start_time % 3600) // 60)
        seconds = int(start_time % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def format_transcript(self, transcript, **kwargs):
        lines = []
        for line in transcript:
            start = int(line["start"])
            start_ts = self.format_timestamp(line["start"])
            timestamp = f"[{start_ts}](https://youtu.be/{kwargs['video_id']}?t={start})"
            text = f"> {line['text'].strip().replace('\n', ' ')}"

            lines.append(f"{timestamp}\n{text}")
        return "\n\n".join(lines)

    def format_transcripts(self, transcripts, **kwargs):
        return self.format_transcript(transcripts, **kwargs)
