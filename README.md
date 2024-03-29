# Cat Music Video Generator

Running instructions:  
$ cd cat_music_video_generator  
$ pip install -r requirements.txt  
$ flask --app main run

The cat music video generator is a Flask webapp that takes any song and creates a lyric video from CAT PICTURES. This project was inspired by [catmusicvideo](https://www.tiktok.com/@catmusicvideo). Here it is in action:

https://github.com/ireneni/cat_music_video_generator/assets/36576160/7d3f5d2f-07bf-4d85-9bc7-a91b8502913c

First, the user searches up the name of a song, and the Genius Lyrics API is used to return the top 3 matches. The user then clicks on the correct song, and this selection is sent to the Python backend where the generation process begins.   
  
The lyrics are first split by line, and each line undergoes tokenization with spaCy. The tokens are analyzed for their part of speech, as we want nouns and adjectives first, then if none are present we take verbs. If the lyric contains multiple hits, the token that occurs more commonly in the English language is chosen. This is accomplished via the wordfreq library, which analyzes the word against its dataset and returns a frequency measure between 0 and 1. A finalized dictionary of tokens is created.  
  
Next, a Selenium webscraper is used to search google images for the term “{token} cat pinterest”. For example, if our song is Taylor Swift’s You Belong With Me, which begins with “You’re on the phone”, the token selected would be “phone”. Thus, the search term is “phone cat pinterest”. The webscraper then grabs the src attribute of the first image result, and the image is downloaded to a local folder. Once an image has been found for each line of the song, the app compiles the images into a slideshow with the corresponding lyric printed under. 


Hope you have fun creating your own cat music videos! 
