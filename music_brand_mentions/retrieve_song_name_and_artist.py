import os
import json
import requests

from bs4 import BeautifulSoup


class MissingDataException(Exception):
    """Raise for output that lacks both song and artist name for each item."""


def retrieve_chart_data(url):

    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'lxml')

    bb_class = 'chart-element__information__{} text--truncate color--{}'

    song_class = bb_class.format('song', 'primary')
    song_names = html.findAll("span", {"class": song_class})
    song_names = [x.get_text().replace(' ', '-').lower() for x in song_names]

    artist_class = bb_class.format('artist', 'secondary')
    artist_names = html.findAll("span", {"class": artist_class})
    artist_names = [x.get_text().replace(' ', '-').lower()
                    for x in artist_names]
    # Need to adjust to handle multiple artists. For example:
    # Current format: https://genius.com/anuel-aa,-daddy-yankee,-karol-g,-ozuna-&-j-balvin-china-lyrics
    # Correct format: https://genius.com/anuel-aa-daddy-yankee-and-karol-g-china-lyrics
    # Even if the order of the artists does not match up with Genius', 
    # it will redirect to a "Page Not Found" page.
    # Create a function "shuffle" that shuffles the artist names and pings the url
    # until a 200 GET request is obtained.

    if len(song_names) != len(artist_names):
        err = 'Missing song or artist information'
        raise MissingDataException(err)

    chart = {song_names[i]: artist_names[i] for i in range(len(song_names))}

    return chart
