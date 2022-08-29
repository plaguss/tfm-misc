"""Script to download videos from youtube.

The videos are downloaded to a separate folder and after the movements
are labeled, removed.

The script must be executed from the root of the project.

References
----------
https://github.com/yt-dlp/yt-dlp#output-template-examples
https://write.corbpie.com/downloading-youtube-videos-and-playlists-with-yt-dlp/

Examples
--------
Download a single video:
# Download only video, best quality up to 480p, extension mp4.
# Redirects to folder videos/
# Download a single video
yt-dlp -f 'bv[height<=480][ext=mp4]' https://www.youtube.com/watch?v=4-5ZJahGp0o&t=1s -o 'videos/%(title)s.mp4'
"""

import pathlib
import subprocess


def fetch_urls():
    urls_path = pathlib.Path.cwd() / "videos" / "urls.txt"
    with open(urls_path) as file:
        lines = [l.rstrip("\n") for l in file.readlines() if not l.startswith("#")]

    return lines


def download(start=0, end=None):
    urls = fetch_urls()
    for url in urls[start:end]:
        print(url)
        cmd = ["yt-dlp"]  # Base command
        cmd += ["-f", "bv[height<=480][ext=mp4]"]  # Formats to download
        cmd += [url]  # Video url
        cmd += ["-o", "videos/%(title)s.mp4"]  # Redirect output
        subprocess.run(cmd, shell=False, check=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Youtube video downloader.")
    parser.add_argument(
        "--start", type=int, default=0, help="start from the video in this position in urls.txt file."
    )
    parser.add_argument(
        "--end", type=int, default=None, help="stop at this video in this position in urls.txt file."
    )

    args = vars(parser.parse_args())

    download(start=args["start"], end=args["end"])
