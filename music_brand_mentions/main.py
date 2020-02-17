import os
import time
import json
import pandas as pd

from utilities import retrieve_saturday_dates
from retrieve_song_lyrics import retrieve_lyrics
from generate_song_urls import get_song_api_path, generate_lyrics_webpage_url
from retrieve_brand_mentions import _count_substring_occurance, count_brand_occurances
from retrieve_song_name_and_artist import (_retrieve_song_names,
                                           _retrieve_artist_names,
                                           retrieve_chart_data)

if __name__ == '__main__':

    dates = []

    for date in retrieve_saturday_dates(2019):
        dates.append(date)

    urls = []

    for date in dates:
        url = f'https://www.billboard.com/charts/r-b-hip-hop-songs/{date}'
        urls.append(url)

    for url in urls:
        time.sleep(4)
        retrieve_chart_data(url, url.split('/')[-1])

    charts = {}

    for date in dates:
        file = open(f'data/charts/{date}.txt').read()
        charts[date] = json.loads(file)

    for date in charts:
        api_paths = []
        for item in charts[date].items():
            try:
                song = item[0].replace('-',' ')
                artist = item[1].replace('-',' ').title()

                api_path = get_song_api_path(song, artist)
                api_paths.append(api_path)

                with open(f'data/urls/{date}_api_paths.txt', 'w') as f:
                    f.writelines("%s," % place for place in api_paths)
                
            except:
                pass

    api_paths = {}

    for date in dates:
        file = open(f'data/urls/{date}_api_paths.txt').read()
        api_paths[date] = file.split(',')

    for date in api_paths:
        lyrics_urls = []
        for item in api_paths[date]:
            try:
                lyrics_urls.append(generate_lyrics_webpage_url(item))

                with open(f'data/lyric_urls/{date}_lyric_urls.txt', 'w') as file:
                    file.writelines("%s," % place for place in lyrics_urls)

            except:
                pass


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

    brand_cts = {}

    dates = [date.strftime("%Y-%m-%d") for date in retrieve_saturday_dates(2019)]

    for date in dates:
        brand_cts[date] = count_brand_occurances(f'data/lyrics/{date}_lyrics.txt')

    pd.DataFrame(brand_cts).to_csv('data.csv')