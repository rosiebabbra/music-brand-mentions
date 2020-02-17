import os
import json
import time
import requests

from bs4 import BeautifulSoup
from utilities import retrieve_saturday_dates


class MissingDataException(Exception):
    """Raise for output that lacks both song and artist name for each item."""


def _retrieve_song_names(url):

    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'lxml')

    soup = html.findAll("span", {"class":"chart-list-item__title-text"})
    song_names = [x.get_text().strip() for x in soup]

    return song_names


def _retrieve_artist_names(url):

    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'lxml')

    soup = html.findAll("div", {"class":"chart-list-item__artist"})
    song_names = [x.get_text().strip() for x in soup]

    return song_names


def retrieve_chart_data(url, week):
    """
    Args:
        url (str): url of Billboard webpage containing hip hop charts.

    Returns:
        dict: key value pairs of each top song and its artist(s).

    """

    song_names = _retrieve_song_names(url)
    artist_names = _retrieve_artist_names(url)

    if len(song_names) != len(artist_names):
        err = 'Missing song or artist information'
        raise MissingDataException(err)

    chart = {song_names[i]: artist_names[i] for i in range(len(song_names))}

    if not os.path.exists('data/charts/'):
        os.makedirs('data/charts/')

    with open(f'data/charts/{week}.txt', 'w') as file:
        file.write(json.dumps(chart))