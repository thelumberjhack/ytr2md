from ytr2md.MdFormatter import MarkDownFormatter


def test_format_timestamp_basic_cases():
    fmt = MarkDownFormatter()
    # The static method is accessed via class for clarity
    assert fmt.format_timestamp(0) == "00:00:00"
    assert fmt.format_timestamp(59.9) == "00:00:59"
    assert fmt.format_timestamp(60) == "00:01:00"
    assert fmt.format_timestamp(3599) == "00:59:59"
    assert fmt.format_timestamp(3661) == "01:01:01"


def test_format_transcript_single_line():
    transcript = [
        {"start": 12.4, "duration": 3.5, "text": "Hello World"},
    ]
    fmt = MarkDownFormatter()
    output = fmt.format_transcript(transcript, video_id="VIDEOID12345")
    assert output.startswith(
        "[00:00:12](https://youtu.be/VIDEOID12345?t=12)\n> Hello World"
    )


def test_format_transcript_multiline_and_newline_stripping():
    transcript = [
        {"start": 0.0, "duration": 4.0, "text": "Line one\nLine two"},
        {"start": 65.2, "duration": 2.0, "text": "Trailing spaces   "},
    ]
    fmt = MarkDownFormatter()
    md = fmt.format_transcript(transcript, video_id="AbCdEfGhIjk")
    parts = md.split("\n\n")
    assert parts[0] == (
        "[00:00:00](https://youtu.be/AbCdEfGhIjk?t=0)\n> Line one Line two"
    )
    assert parts[1] == (
        "[00:01:05](https://youtu.be/AbCdEfGhIjk?t=65)\n> Trailing spaces"
    )
    # Ensure exactly two blocks
    assert len(parts) == 2
