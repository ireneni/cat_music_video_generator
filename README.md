# Cat Music Video Generator

The cat music video generator is a Flask webapp that takes any song and creates a lyric video with CAT PICTURES. This project was inspired by [catmusicvideo](https://www.tiktok.com/@catmusicvideo).

<img width="500" alt="Screen Shot 2023-09-13 at 3 36 34 PM" src="https://github.com/ireneni/cat_music_video_generator/assets/36576160/a09e17e8-0fd6-42d4-a881-8176b7458c9c">

First, the user searches up the name of a song, and the Genius Lyrics API is used to return the top 3 matches. The user then clicks on the correct song, and this selection is sent to the Python backend where the generation process begins.   
  
The lyrics are first split by line, and each line undergoes tokenization with spaCy. The tokens are analyzed for their part of speech, as we only want nouns and adjectives. If the lyric contains multiple hits, the token that occurs more commonly in the English language is chosen. This is accomplished via the wordfreq library, which analyzes the word against its dataset and returns a frequency measure between 0 and 1. A finalized dictionary of tokens is created.  
  
Next, a Selenium webscraper is used to search google images for the term “{token} cat pinterest”. For example, if our song is Taylor Swift’s You Belong With Me, which begins with “You’re on the phone”, the token selected is “phone”. Therefore, the search term is “phone cat pinterest”. The webscraper then grabs the src of the first image result, and the image is downloaded to a local folder. Once an image has been found for each line of the song, the app compiles the images into a slideshow with the corresponding lyric printed under. Here it is in action:


https://github.com/ireneni/cat_music_video_generator/assets/36576160/55105056-57b0-4735-86f6-61a8704ee5a0
  
Hope you have fun creating your own cat music videos! 

