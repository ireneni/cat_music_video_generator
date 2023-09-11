from flask import Flask, render_template, request
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


def lyrics_search(search_term):
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

    # print(data_json['response']['hits'][0]['result'].keys())
    title = data_json['response']['hits'][0]['result']['title']
    artist = data_json['response']['hits'][0]['result']['artist_names']
    url = data_json['response']['hits'][0]['result']['url']
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")  # Extract the page's HTML as a string
    # Scrape the song lyrics from the HTML
    soup = html.find_all("div", attrs={'class': re.compile('^Lyrics__Container.*')})
    lyrics = '\n'.join(item.getText(separator='\n') for item in soup)
    return title, artist, lyrics


def split_lyrics_by_line(lyrics):
    s = lyrics.split('\n')
    split_lyrics = []
    chars_to_replace = {'(': '', ')': '', '\u2005': ' ', '\\': ''}
    for x in s:
        if '[' in x:
            continue
        elif len(x) < 3:
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
        doc = nlp(split_lyrics[i].lower())
        for token in doc:
            if token.text in nlp.Defaults.stop_words or token.text in punctuation:
                continue
            if token.pos_ in pos_tag:
                if i in result.keys():
                    result[i] = get_more_common_word(result[i], token.text)
                else:
                    result[i] = token.text
    return result


def get_more_common_word(a, b):
    freq_a = wordfreq.word_frequency(a, 'en')
    freq_b = wordfreq.word_frequency(b, 'en')
    if freq_a > freq_b:
        return a
    else:
        return b


def scrape_images(keyword_dict):
    for key in keyword_dict:
        image_search.download_google_images(
            keyword_dict[key] + ' cat pinterest',
            key
        )

#
# lyrics_result = lyrics_search('Mamma Mia')
# lyrics_split = split_lyrics_by_line(lyrics_result[2])
# keywords = extract_keywords(lyrics_split)
# print(scrape_images(keywords))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_query', methods=['GET', 'POST'])
def get_song_query():
    if request.method == 'POST':
        song_name = request.form
        return render_template('create.html')

