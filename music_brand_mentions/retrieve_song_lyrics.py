import os
import re
import json
import requests
from retrieve_song_name_and_artist import retrieve_chart_data

from bs4 import BeautifulSoup


def generate_urls():

    url = 'https://genius.com/{}-{}-lyrics'

    charts = retrieve_chart_data()

    urls = [url.format(pair[1], pair[0]) for pair in charts.items()]
    valid_urls = [x for x in urls if requests.get(x).status_code == 200]

    pct_valid_urls = round(len(valid_urls)/len(urls), 1)

    if pct_valid_urls < .75:
        raise Exception(f'Only {pct_valid_urls}% of urls were in valid format')

    return valid_urls


def retrieve_lyrics(url):

    doc = requests.get(url)
    html = BeautifulSoup(doc.text, 'lxml')

    lyrics = html.find("div", class_="lyrics").get_text()

    cleaned_lyrics = re.findall(r'([^[\]]+)(?:$|\[)', lyrics)
    cleaned_lyrics = ' '.join(cleaned_lyrics)\
                        .replace('\n', ' ')\
                        .replace('(', '')\
                        .replace(')', '')\
                        .replace(',', '')\
                        .replace('?', '')

    return cleaned_lyrics