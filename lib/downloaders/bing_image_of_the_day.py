#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import requests
import sys
import urllib.parse

sys.path.insert(1, '../lib')
import wariety_wallpaper

START_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
BASE_URL = 'https://www.bing.com'
DOWNLOADER_TYPE = 'bing'
CAPABILITIES = {'single': 'single', 'many': 'many'}

def get_next_image(last_image_counter=0):
    """Retrieves a BING picture of the day and returns it
    as an instance of wariety wallpaper. Depending on the counter
    given by 'last_image_counter' returns the next picture.
    """
    next_image = wariety_wallpaper.WarietyWallpaper()
    response = requests.get(START_URL)
    image_data = json.loads(response.text)

    image_url = image_data["images"][0]["url"]
    image_url = image_url.split("&")[0]
    image_title = image_data["images"][0]["title"]
    image_copyright = image_data["images"][0]["copyright"]
    if image_title:
        image_title = image_title + '.'
    if image_copyright:
        image_copyright = image_copyright + '.'
    try:
        next_image.image_name = urllib.parse.unquote(urllib.parse.urljoin(BASE_URL, image_url)).split('/')[-1].split('=')[-1]
    except:
        next_image.image_name = ''
    next_image.source_url = urllib.parse.unquote(image_url)
    next_image.source_type = DOWNLOADER_TYPE
    next_image.image_author = ''
    next_image.source_name = 'Bing Bild des Tages'
    next_image.image_url = urllib.parse.unquote(urllib.parse.urljoin(BASE_URL, image_url))
    next_image.location = ''
    next_image.keywords = '{0} {1}'.format(image_title,image_copyright).strip()
    next_image.source_location = ''
    next_image.found_at_counter = last_image_counter + 1
    return next_image

def get_downloader_type():
    return DOWNLOADER_TYPE

def get_capability():
    return CAPABILITIES['single']