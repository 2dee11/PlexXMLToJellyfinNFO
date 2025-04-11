# Plex XML To Jellyfin .NFO Files

I, probably like you reading this, wanted to convert my Plex library to Jellyfin without losing all of my years or hard work setting up Titles, Sort Titles, Original Titles, Added At Dates, Last Viewed At Dates, View Counts, and Collections.

This collection of scripts will help you do just that as easily as possible. 

Please note that I am by no means a developer, just an idiot on the internet with access to ChatGPT and a little know how. I tried to segment this as much as possible to try and prevent issues but use at your own risk. Someone smarter could probably do all of this in one script but I liked breaking it up into segments.

It probably would have been faster for me to just do this manually instead of try and script it but I knew others like me probably wanted this too. I couldn't find anything simple that would do what I wanted. I hope this works for you.


# Get your Plex XML Data
First create a folder that we will be using for now on. I used C:\temp

We need to know the library IDs for all libraries you'd like to export. <ins>I only tested this on movie libraries.</ins> Open CMD and run the following. Be sure to replace with your IP and Plex Token.

`cd c:\temp`

`curl -o libraries.xml "http://YOURPLEXIPANDPORT/library/sections?X-Plex-Token=YOURPLEXTOKEN`

Now you can open up the libraries.xml file and see the libraries and their numbers, if you only have one movie library its typically ID 1. Look for a snippet like below.

`key="1"`

Next we can run the following command in CMD to pull all metadata for all items in the selected library by ID. Be sure to replace with your IP and Plex Token also replace the number after sections/ with the library ID you'd like to pull metadata for. <ins>Again, I only tested this on movie libraries.</ins>

`curl -o metadata.xml "http://YOURPLEXIPANDPORT/library/sections/1/all?X-Plex-Token=YOURPLEXTOKEN`

You will now have a file named metadata.xml in your C:\temp folder. You can review this now to make sure everything looks good. 


# Optional: Convert XML to List of Collections
This was the original goal before I decided to take this a step further. This will simply pull a list of collections from the Plex metadata.xml file and export it as a .txt. You will need python installed on your PC.

Save the PlexCollections.py script to your C:\temp and run the following in CMD.

`py PlexCollections.py > PlexCollections.txt`

From here you could use this list to manually create the collections in Jellyfin. 


# Optional: Convert XML to List of Collections with Movies that are in each Collection. 
Again, this was another in between step that seems like it could be useful for someone. This will pull a list of collections and the movies that belong to each collection from the Plex metadata.xml file and export it as a .txt. You will need python installed on your PC.

Save the PlexMovieswithCollections.py script to your C:\temp and run the following in CMD.

`py PlexMovieswithCollections.py > PlexMovieswithCollections.txt`

Again you could use this list to manually create the collections in Jellyfin. 


# Convert XML to List of Movies with Relevant Data
This script will take the metadata.xml and export a .txt list of movies with their Title, Sort Title, Original Title, Added At Date, Last Viewed At Date, View Count, Collections and File Path as applicable. Again this step is a bit repetitive as you could likely go straight from the xml to .NFO files but I liked to use this as a check to make sure everything looks good. I would also recommend doing a trial run by editing this file and having only one movie in the list to test the next step. 

Save the PlexXMLPull.py script to your C:\temp and run the following in CMD.

`py PlexXMLPull.py > PlexXMLPull.txt`

You should now have a file named PlexXMLPull.txt with a list of all your movies and their data. 


# Convert Movie List and Data to .NFO Files and Store them in their Respective Folders. 
This script will take the PlexXMLPull.txt file and convert the data to individual .NFO files and store them in the Path listed in the PlexXMLPull.txt. I would recommend editing your PlexXMLPull.txt to only have one movie to test before running against all movies. Also depending on where your movies are stored and how your are running Plex/Jellyfin you may need to edit the file paths. For me I run Plex/Jellyfin in docker and they see the movie path as /data/movies but in reality on my Windows machine this is Z:/Media/Movies I had to do a find and replace on /data/movies to replace it to Z:/Media/Movies I didn't want to hardcode this as everyone's path is different. 

Note: you may get a few "Directory does not exist" errors for folder names with special characters like Alien<sup>3</sup> or Joker: Folie à Deux. Check the output in CMD, I just fixed these manually myself within Jellyfin.

Save the JellyfinNFOCreator.py script to your C:\temp and run the following in CMD

`py JellyfinNFOCreator.py`

You should now have a MOVIENAME.NFO file in every folder directory. In Jellyfin, if you scan your libraries and select replace all metadata it should use the .NFO files and your movies should be just as they were in Plex. I will admit that Collections didn't work great for me and I still had to do a decent amount of manual cleanup. I believe you also still need to have the TMDb Box Sets Plugin installed to use any collections in Jellyfin, or at least get any metadata for them. 

After this initial bulk "upload" I would suggest going into settings and selecting Manage Library for each Library and under Metadata Savers section check Nfo. This will create a new .nfo file called movie.nfo for each Movie. Now from this point on any changes you make Jellyfin will keep those new movie.nfo files updated.


# Repeat For All Other Needed Libraries
You will need to go back to the beginning and use the library ID for the other libraries you want. <ins>Again, this was never tested with TV Shows.</ins> You will then get a new metadata.xml file and run your python scripts again.

# Troubleshooting
I had some issues with accessing a network drive to store the files in. Running the below command in CMD helped figure out which drives were accessible or not and troubleshooting accordingly. I also found using regular CMD and not running it as ADMIN was best. YMMV

`net use`


# Final Note
I do not plan on maintaining this and updating this with every change to Plex or Jellyfin, if someone else proposes changes I will try and add them.
