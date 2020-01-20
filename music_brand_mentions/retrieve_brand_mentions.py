import os
import json

from utilities import retrieve_saturday_dates


def _count_substring_occurance(text, substr):
    """Loop through every file in 'data/lyrics' to count 
    the occurances of each brand in each file.
    
    Args:
        text (str): file from which to search substrings
        substr (str): desired substring to be found

    Returns:
        int: Number of occurances of substring in text document.
    
    """

    return text.count(substr)


def count_brand_occurances(file_path):
    """
    Args:
        file_path (str): location of file to be read in

    Returns:
        dict: Occurances per brand.
    
    """

    text = open(file_path).read()

    with open('data/brands.json') as brand_file:
        brands = json.load(brand_file)['brands']

    brand_ct = {}

    for brand in brands:
        brand_ct[brand] = _count_substring_occurance(text, brand)

    return brand_ct


if __name__ == '__main__':

    brand_cts = {}

    dates = [date.strftime("%Y-%m-%d") for date in retrieve_saturday_dates(2019)]

    for date in dates:
        brand_cts[date] = count_brand_occurances(f'data/lyrics/{date}_lyrics.txt')