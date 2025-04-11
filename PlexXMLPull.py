import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Parse the XML file
tree = ET.parse('metadata.xml')
root = tree.getroot()

# Track if we're on the first movie to control spacing
first = True

# Iterate over all 'Video' elements (representing movies)
for video in root.findall(".//Video"):
    # Extract movie details from attributes
    movie_title = video.get('title')
    title_sort = video.get('titleSort')
    original_title = video.get('originalTitle')
    added_at = video.get('addedAt')
    view_count = video.get('viewCount')
    last_viewed_at = video.get('lastViewedAt')
    
    # Format addedAt date
    if added_at:
        added_at_date = datetime.fromtimestamp(int(added_at), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    else:
        added_at_date = None

    # Format lastViewedAt date
    if last_viewed_at:
        last_viewed_date = datetime.fromtimestamp(int(last_viewed_at), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    else:
        last_viewed_date = None

    # Get the file path for the movie from the 'Part' element (if present)
    part_element = video.find(".//Part")
    file_path = part_element.get('file') if part_element is not None else "No file path"

    # Extract the collection tags (if present)
    collection_elements = video.findall(".//Collection")
    collection_tags = [collection.get('tag') for collection in collection_elements]
    collections = ", ".join(collection_tags) if collection_tags else None

    # Add blank line before movie entry, except for the first one
    if not first:
        print()
    first = False

    # Print extracted movie information
    print(f"Movie Title: {movie_title}")

    if title_sort:
        print(f"  TitleSort: {title_sort}")
    if original_title:
        print(f"  OriginalTitle: {original_title}")
    if added_at_date:
        print(f"  AddedAt: {added_at_date}")
    if last_viewed_date:
        print(f"  LastViewedAt: {last_viewed_date}")
    if view_count:
        print(f"  ViewCount: {view_count}")
    if collections:
        print(f"  Collections: {collections}")

    print(f"  File Path: {file_path}")
