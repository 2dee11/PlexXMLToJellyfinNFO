import xml.etree.ElementTree as ET
from collections import defaultdict

# Parse the XML file
tree = ET.parse('metadata.xml')
root = tree.getroot()

# Initialize a dictionary to group movies by collection name
collections_grouped = defaultdict(list)

# Iterate over all 'Video' elements (representing movies)
for video in root.findall(".//Video"):
    # Get the movie title from the 'title' attribute
    movie_title = video.get('title')
    
    if movie_title:
        # Check if the movie has a 'Collection' tag (looking for the 'tag' attribute)
        collection_elements = video.findall(".//Collection")
        
        # For each collection, get the 'tag' attribute (collection name)
        for collection in collection_elements:
            collection_name = collection.get('tag')
            if collection_name:
                # Add the movie title to the list of movies for this collection
                collections_grouped[collection_name].append(movie_title)

# Print movies grouped by collection name
if collections_grouped:
    print("\nMovies grouped by Collection:")
    for collection_name, movies in collections_grouped.items():
        print(f"\nCollection: {collection_name}")
        for movie in movies:
            print(f"  {movie}")
else:
    print("No movies with a collection tag found.")
