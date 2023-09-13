from flask import Flask, render_template, request, jsonify, redirect, url_for
import urllib
import json
import requests
import re
from bs4 import BeautifulSoup
import spacy
from string import punctuation
import wordfreq
import image_search

app = Flask(__name__)


def song_search(search_term):
    # Format a request URI for the Genius API
    _URL_API = "https://api.genius.com/"
    _URL_SEARCH = "search?q="
    querystring = _URL_API + _URL_SEARCH + urllib.parse.quote(search_term)
    request = urllib.request.Request(querystring)
    client_access_token = "3YcqTiRnqMZj9Bn6q31mVR_rPnKlSglUtiajoCuoXR4WXyp8odYNatOZfYq1_KMz"
    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "")

    response = urllib.request.urlopen(request, timeout=3)

    data_json = json.loads(response.read())

    song_dict = {}
    for i in range(3):
        song_dict['song-' + str(i)] = str(i+1) + '. ' + data_json['response']['hits'][i]['result']['title'] + ' by ' + data_json['response']['hits'][i]['result']['artist_names']
        song_dict['url-' + str(i)] = data_json['response']['hits'][i]['result']['url']

    return song_dict


def get_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")  # Extract the page's HTML as a string
    # Scrape the song lyrics from the HTML
    soup = html.find_all("div", attrs={'class': re.compile('^Lyrics__Container.*')})
    lyrics = '\n'.join(item.getText(separator='\n') for item in soup)

    return lyrics


def split_lyrics_by_line(lyrics):
    s = lyrics.split('\n')
    split_lyrics = []
    chars_to_replace = {'(': '', ')': '', '\u2005': ' ', '\\': ''}
    for x in s:
        if '[' in x:
            continue
        elif len(x) < 2:
            continue
        else:
            for key, val in chars_to_replace.items():
                x = x.replace(key, val)
            split_lyrics.append(x)
    return split_lyrics


def extract_keywords(split_lyrics):
    nlp = spacy.load("en_core_web_sm")
    result = {}
    pos_tag = ['PROPN', 'ADJ', 'NOUN']
    for i in range(len(split_lyrics)):
        if i > 1:
            break
        doc = nlp(split_lyrics[i])
        for token in doc:
            if token.text in nlp.Defaults.stop_words or token.text in punctuation:
                continue
            if token.pos_ in pos_tag or token.dep_ == 'pcomp':
                if i in result.keys():
                    result[i] = get_more_common_word(result[i], token.text)
                else:
                    result[i] = token.text
    return result


def get_more_common_word(a, b):
    if len(a) < 3 < len(b):
        return b
    if len(b) < 3 < len(a):
        return a
    freq_a = wordfreq.word_frequency(a, 'en')
    freq_b = wordfreq.word_frequency(b, 'en')
    if freq_a > freq_b:
        return a
    else:
        return b


init_data = {}


@app.route('/')
def index():
    return render_template('index.html', data=init_data)


@app.route('/get_query', methods=['POST'])
def get_song_query():
    if request.method == 'POST':
        song_name = request.form.get('search')
        songs = song_search(song_name)
        return render_template('index.html', data=songs)


@app.route('/process_selection', methods=['POST'])
def process_selection():
    if request.method == 'POST':
        url = request.json.get('selectedItem')
        lyrics = get_lyrics(url)
        lyrics_split = split_lyrics_by_line(lyrics)
        keywords = extract_keywords(lyrics_split)
        image_files_dict = image_search.scrape_images(keywords)
        lyrics_dict = dict(enumerate(lyrics_split[:2]))
        # return redirect(url_for('display_slideshow', lyrics=lyrics_dict, images=image_files_dict))


@app.route('/slideshow', methods=['GET'])
def display_slideshow():
    print('display slideshow is executing')
    lyrics = request.args.get('lyrics')
    images = request.args.get('images')
    return render_template('slideshow.html', lyrics=lyrics, images=images)


if __name__ == '__main__':
    app.run(debug=True)