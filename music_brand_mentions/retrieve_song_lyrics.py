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


if __name__ == '__main__':

    urls = {}

    dates = [date.strftime("%Y-%m-%d") for date in retrieve_saturday_dates(2019)]

    for date in dates:
        file = open(f'data/lyric_urls/{date}_lyric_urls.txt').read()
        urls[date] = file.split(',')

    for date in urls:
        lyrics = []
        for url in urls[date]:
            try:
                lyrics.append(retrieve_lyrics(url))
                with open(f'data/lyrics/{date}_lyrics.txt', 'w') as file:
                    file.writelines("%s|" % place for place in lyrics)
            except:
                pass