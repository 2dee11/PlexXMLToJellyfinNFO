import os
import re
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

INPUT_FILE = 'PlexXMLPull.txt'  # your .txt file

def parse_movies(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    movie_blocks = re.split(r'\n(?=Movie Title:)', content.strip())
    movies = []

    for block in movie_blocks:
        lines = block.strip().split('\n')
        data = {'Collections': []}
        for line in lines:
            if line.startswith('Movie Title:'):
                data['title'] = line.split(':', 1)[1].strip()
            elif ':' in line:
                key, value = line.strip().split(':', 1)
                key = key.strip()
                value = value.strip()
                if key == 'Collections':
                    data['Collections'].append(value)
                else:
                    data[key] = value
        movies.append(data)

    return movies


def create_nfo(movie):
    root = Element('movie')

    SubElement(root, 'title').text = movie.get('title', '')
    if 'OriginalTitle' in movie:
        SubElement(root, 'originaltitle').text = movie['OriginalTitle']
    if 'TitleSort' in movie:
        SubElement(root, 'sorttitle').text = movie['TitleSort']
    if 'AddedAt' in movie:
        SubElement(root, 'dateadded').text = movie['AddedAt']
    if 'LastViewedAt' in movie:
        SubElement(root, 'lastplayed').text = movie['LastViewedAt']
    if 'ViewCount' in movie:
        SubElement(root, 'playcount').text = movie['ViewCount']

    if movie.get('Collections'):
        for collection in movie['Collections']:
            set_element = SubElement(root, 'set')
            SubElement(set_element, 'name').text = collection  # Properly using <name> inside <set>

    return root


def write_nfos(movies):
    for movie in movies:
        file_path = movie.get('File Path')
        if not file_path:
            print(f"Skipping {movie.get('title')} - no file path.")
            continue

        nfo_path = Path(file_path).with_suffix('.nfo')
        nfo_dir = nfo_path.parent

        if not nfo_dir.exists():
            print(f"Directory does not exist: {nfo_dir}")
            continue

        xml_root = create_nfo(movie)
        tree = ElementTree(xml_root)
        tree.write(nfo_path, encoding='utf-8', xml_declaration=True)
        print(f"Wrote NFO: {nfo_path}")


if __name__ == '__main__':
    movies = parse_movies(INPUT_FILE)
    write_nfos(movies)
