#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import logging
import requests
import sys
import urllib.parse

sys.path.insert(1, '../.')
import wariety_wallpaper
from downloaders.default_downloader import DefaultDownloader

START_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
BASE_URL = 'https://www.bing.com/HPImageArchive.aspx'
DOWNLOADER_TYPE = 'bing'
DOWNLOADER_DESCRIPTION = 'Bing Image Of The Day'
CAPABILITIES = {'single': 'single', 'many': 'many'}

logger = logging.getLogger(__name__)

class BingDownloader(DefaultDownloader):

    def get_downloader_type(self):
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        return CAPABILITIES['single']

    def get_base_url(self):
        return BASE_URL

    def get_next_image(self, last_image_counter=0):
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
