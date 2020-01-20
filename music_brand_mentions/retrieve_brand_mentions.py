import os
import json

from utilities import retrieve_saturday_dates


def _count_brands(text, substr):
    """Loop through every file in 'data/lyrics' to count 
    the occurances of each brand in each file."""

    return text.count(substr)


def read_lyrics_file(file):

    text = open(file).read()

    with open('data/brands.json') as brand_file:
        brands = json.load(brand_file)['brands']

    brand_ct = {}

    for brand in brands:
        brand_ct[brand] = _count_brands(text, brand)

    return brand_ct


if __name__ == '__main__':

    brand_cts = {}

    dates = [date.strftime("%Y-%m-%d") for date in retrieve_saturday_dates(2019)]

    for date in dates:
        brand_cts[date] = read_lyrics_file(f'data/lyrics/{date}_lyrics.txt')