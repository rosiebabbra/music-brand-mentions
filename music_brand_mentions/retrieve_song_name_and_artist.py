import os
import json
import requests

from bs4 import BeautifulSoup


class MissingDataException(Exception):
    """Raise for output that lacks both song and artist name for each item."""


def _return_chart_metadata(meta, level):
    """Gathers information about top music charts.

    Args:
        meta (str): 'song' or 'artist'
        level (str): 'primary' or 'secondary

    Returns:
        List: collection of metadata from charts page.

    """

    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'lxml')

    meta_class = f'chart-element__information__{meta} text--truncate color--{level}'

    meta = html.findAll("span", {"class": meta_class})
    meta_collection = [x.get_text().replace(' ', '-').lower() for x in meta]

    return meta_collection


def retrieve_chart_data(url):
    """
    Args:
        url (str): url of Billboard webpage containing U.S. charts.

    Returns:
        Dict: key value pairs of each top song and its artist(s).

    """

    song_names = _return_chart_metadata('song', 'primary')
    artist_names = _return_chart_metadata('artist', 'secondary')
    
    # Need to adjust to handle multiple artists. For example:
    
    # Current format: https://genius.com/anuel-aa,-daddy-yankee,-karol-g,-ozuna-&-j-balvin-china-lyrics
    # Correct format: https://genius.com/anuel-aa-daddy-yankee-and-karol-g-china-lyrics
    
    # If even the order of the artists does not match up exactly 
    # with Genius', the URL will not return the lyrics.
    
    # Create a method "shuffle" that shuffles the artist names 
    # and pings the url until a 200 GET request is obtained.

    if len(song_names) != len(artist_names):
        err = 'Missing song or artist information'
        raise MissingDataException(err)

    chart = {song_names[i]: artist_names[i] for i in range(len(song_names))}

    return chart