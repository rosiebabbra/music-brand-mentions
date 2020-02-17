import os
import re
import json
import requests

from bs4 import BeautifulSoup
from utilities import retrieve_saturday_dates
from retrieve_song_name_and_artist import retrieve_chart_data


def retrieve_lyrics(url):
    """Retrieves lyrics from a provided Genius url.

    Args:
        url (str): url of Genius webpage containing lyrics
    Returns:
        str: Stringified and cleaned lyrics.

    """

    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'lxml')

    lyrics = html.find("div", class_="lyrics").get_text()

    cleaned_lyrics = re.findall(r'([^[\]]+)(?:$|\[)', lyrics)
    cleaned_lyrics = ' '.join(cleaned_lyrics)\
                        .replace('\n', ' ')\
                        .replace('(', '')\
                        .replace(')', '')\
                        .replace(',', '')\
                        .replace('?', '')\
                        .lower()

    return cleaned_lyrics