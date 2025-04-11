import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('metadata.xml')
root = tree.getroot()

# Initialize a set to store unique collection names
collections = set()

# Iterate over all 'Collection' elements
for collection in root.findall(".//Collection"):
    # Get the 'tag' attribute (which contains the collection name)
    collection_name = collection.get('tag')
    if collection_name:
        collections.add(collection_name)

# Print all collection names
for collection in collections:
    print(collection)
