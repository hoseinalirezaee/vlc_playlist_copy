import shutil
import sys
from pathlib import Path
from time import time
from typing import List
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


def get_tracks_path_list(playlist_file):
    playlist_xml = ElementTree.parse(playlist_file)
    locations = playlist_xml.findall('.//location', namespaces={'': 'http://xspf.org/ns/0/'})
    paths = [Path(urlsplit(unquote(loc.text)).path) for loc in locations]
    return paths


def sizeof_fmt(num, suffix='B'):
    """
    Copied from https://stackoverflow.com/a/1094933
    """

    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def get_total_size(tracks: List[Path]):
    total_size = 0
    for track in tracks:
        total_size += track.stat().st_size
    return total_size


def copy_tracks(tracks: List[Path], destination_dir: Path):
    total_size = get_total_size(tracks)
    copied_size = 0
    start_time = time()
    for track in tracks:
        shutil.copy(track.absolute(), destination_dir.absolute())
        current_time = time()
        speed = sizeof_fmt(copied_size / (current_time - start_time), 'B / s')
        copied_size += track.stat().st_size
        print('Copied %s from %s ... speed: %s' % (sizeof_fmt(copied_size), sizeof_fmt(total_size), speed))


def main():
    playlist_file = Path(sys.argv[1])
    destination_directory = Path(sys.argv[2])
    if not destination_directory.exists():
        destination_directory.mkdir()
    with open(playlist_file) as file:
        tracks = get_tracks_path_list(file)
        copy_tracks(tracks, destination_directory)


if __name__ == '__main__':
    main()
