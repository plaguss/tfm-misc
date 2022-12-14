r"""Transforms the json of annotations from supervisely to a format
that can be ingested by ffmpeg-split.py

Needs a path to a file, and the total number of frames.

Example to create the manifest.json
$ python scripts/manifester.py --annotations "CF-moves_ds0_Friendly Fran - Online Semifinals Event 1_Bryan Hernandez.mp4.json"

If run without arguments, executes the code for each file in
the annotations directory:
$ python scripts/manifester.py

"""

import json
import pathlib
import subprocess
import sys
import warnings

import tqdm


ROOT = pathlib.Path.cwd()
CLIPS_FOLDER = ROOT / "clips"
ANNOTATIONS_FOLDER = ROOT / "annotations"
VIDEOS_FOLDER = ROOT / "videos"


def frames_to_secs(frames: int, total_frames: int, time_secs: int) -> float:
    """Transforms the number position in frames to seconds.

    Utility to transform from the information given from
    supervisely, to the info needed by ffmpeg-split.py.

    frame_to_secs(1329)

    Parameters
    ----------
    frames : int
        Number of frames to convert to seconds.
    total_frames : int
        Total number of frames of the video, as seen in supervisely.
    time_secs : int
        Total length of the video, in seconds.

    Returns
    -------
    secs
        Seconds equivalent to the frames.
    """
    return (frames / total_frames) * time_secs


def load_annotations(annotations: str):
    """Loads the annotations generated by supervisely.

    It must be a json stored in annotations directory, with the same
    name of the video it came from, and .json extension.

    Parameters
    ----------
    annotations : str
        Name of the video annotations in annotations/ folder.
    """
    annot = ANNOTATIONS_FOLDER / annotations

    if not annot.is_file():
        raise FileNotFoundError(f"annotations file not found: {annot}")

    with open(annot, "r") as f:
        data = json.load(f)

    return AnnotationsFile(data)


class AnnotationsFile:
    """Class representing the annotations file returned by supervisely."""

    def __init__(self, data: dict) -> None:
        self._data = data
        self._last_ids = {}

    def __repr__(self) -> str:
        return type(self).__name__ + f"({self._data['videoName']})"

    @property
    def name(self) -> str:
        return self._data["videoName"]

    @property
    def frames(self) -> int:
        return self._data["framesCount"]

    @property
    def duration(self) -> float:
        """Returns the duration in seconds."""
        return get_video_duration(str(VIDEOS_FOLDER / self.name))

    @property
    def movements(self):
        return set([t["name"] for t in self._data["tags"]])

    def get_last_id(self, movement) -> int:
        if not movement in self._last_ids:
            try:
                self._last_ids[movement] = max(
                    int(vid.stem.split("_")[-1])
                    for vid in (CLIPS_FOLDER / movement).iterdir()
                )
            except ValueError:
                self._last_ids[movement] = 0

        self._last_ids[movement] += 1
        return self._last_ids[movement]

    def create_manifest(self) -> None:
        total_duration_secs = self.duration
        manifest = []
        for tag in self._data["tags"]:
            name = tag["name"]
            rename_to = f"clips/{name}/{name}_{self.get_last_id(name)}.mp4"
            start_frame, end_frame = tag["frameRange"]
            start_time = frames_to_secs(start_frame, self.frames, total_duration_secs)
            length = frames_to_secs(
                end_frame - start_frame, self.frames, total_duration_secs
            )
            manifest.append(
                {"start_time": start_time, "length": length, "rename_to": rename_to}
            )

        with open(str(ANNOTATIONS_FOLDER / "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=4)


def generate_clips(video: str) -> None:
    cmd = [sys.executable, "scripts/ffmpeg-split.py"]  # Program
    cmd += ["-v", "h264"]  # appropriate format for mp4

    video_ = VIDEOS_FOLDER / video
    if not video_.is_file():
        raise FileNotFoundError(f"video not found: {video_}")

    cmd += ["-f", video_]  # video target

    manifest = ANNOTATIONS_FOLDER / "manifest.json"
    if not manifest.is_file():
        raise FileNotFoundError(f"manifest not found: {video_}")

    cmd += ["-m", manifest]  # video target

    subprocess.run(cmd, shell=False, check=True)


def get_video_duration(video: str) -> float:
    """Returns the exact duration of a video file

    References:
    https://stackoverflow.com/questions/31024968/using-ffmpeg-to-obtain-video-durations-in-python
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            video,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Clip extractor from annotated videos."
    )
    parser.add_argument(
        "--annotations",
        type=str,
        help="Name of the annotations file. Must be found in annotations/ folder.",
    )

    args = vars(parser.parse_args())

    if args.get("annotations") is not None:
        annotations: AnnotationsFile = load_annotations(args["annotations"])

        annotations.create_manifest()
        generate_clips(annotations.name)
    else:
        print("No path was given, running for every file in annotations.")
        
        for f in tqdm.tqdm(list(ANNOTATIONS_FOLDER.iterdir())):

            if not f.name.endswith("mp4.json"):
                # Expected extension of annotation files
                continue

            annotations: AnnotationsFile = load_annotations(f)

            try:
                annotations.create_manifest()
                generate_clips(annotations.name)
            except Exception as exc:
                warnings.warn(f"Something failed creating the annotations for: {f}.")
                print(exc)
