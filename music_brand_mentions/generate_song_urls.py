import os
import json
import requests

from utilities import retrieve_saturday_dates
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv('GENIUS_KEY')

base_url = "http://api.genius.com"
headers = {'Authorization': f'Bearer {TOKEN}'}

dates = [date.strftime("%Y-%m-%d") for date in retrieve_saturday_dates(2019)]


def get_song_api_path(song, artist):
    """Utilize the Genius API to generate valid urls."""

    search_url = f"{base_url}/search"
    data = {'q': song}

    response = requests.get(search_url, params=data, headers=headers)
    results = json.loads(response.text.replace(u'\xa0', u' '))

    for hit in results["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist:
            song_api_path = hit["result"]["api_path"]
            return song_api_path
        else:
            raise Exception('Unable to retrieve lyrics path')


def generate_lyrics_webpage_url(song_api_path):
    """
    Args:
        song_api_path (str): url containing Genius song id

    Returns:
        str: url containing lyrics for given song.

    """

    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)

    json = response.json()
    path = json["response"]["song"]["path"]

    url = "http://genius.com" + path

    return url