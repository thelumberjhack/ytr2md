# Youtube Transcripts 2 MarkDown

A Python CLI tool to format YouTube video transcripts to Markdown.

It will only download manually created english transcripts if they exist.

## ⚠️ Disclaimer

This tool uses the [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) which implements
an unofficial YouTube API so this tool could break anytime. I am not guaranteeing that I will be on top of it unless
it impacts my workflow directly.

With that being said...

## Installation

```shell
git clone git@github.com:thelumberjhack/ytr2md.git
cd ytr2md
rye init
rye sync
rye run ytr2md get <video_id>
```

## Usage

```shell
Usage: ytr2md [OPTIONS] COMMAND [ARGS]...

  Default CLI for ytr2md.

Options:
  -v, --verbose           Enable verbose output.
  -o, --output DIRECTORY  Output dir to save the transcripts.
  --help                  Show this message and exit.

Commands:
  get  Download and format the transcript of a YouTube video.
```

```shell
Usage: ytr2md get [OPTIONS] VIDEO_ID

  Download and format the transcript of a YouTube video.                                  
Options:
  --help  Show this message and exit.
```

## Credits

Full credits go to [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) as this tool is just a nice wrapper around it.
