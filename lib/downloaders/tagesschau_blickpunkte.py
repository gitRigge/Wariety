#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Wariety - A wallpaper manager for MS Windows operating system.
# Copyright (C) 2020  Roland Rickborn <wariety@gmx.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

import datetime
import json
import logging
import re
import sys
import urllib.parse
import urllib.request

import bs4

logger = logging.getLogger(__name__)
if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


START_URL = 'https://www.tagesschau.de/multimedia/bilder/'
BASE_URL = 'https://www.tagesschau.de/'
DOWNLOADER_TYPE = 'tagesschau'
DOWNLOADER_DESCRIPTION = 'Tagesschau - Aktuelle Blickpunkte'
CAPABILITIES = {'single': 'single', 'many': 'many'}


class TagesschauBlickpunkteDownloader(DefaultDownloader):

    def __init__(self, config=None):
        self.config = config
        self._load_state(DOWNLOADER_TYPE)
        super().__init__(config)

    def __del__(self):
        self.save_state(DOWNLOADER_TYPE)

    def get_downloader_type(self):
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        return CAPABILITIES['many']

    def get_base_url(self):
        return BASE_URL

    def get_next_image(self, last_image_counter=0):
        """
        Retrieves a BING picture of the day and returns it
        as an instance of wariety wallpaper. Depending on the counter
        given by 'last_image_counter' returns the next picture.
        :param last_image_counter:
        :return next_image:
        """
        next_image = wariety_wallpaper.WarietyWallpaper()
        try:
            startdate = self.state['startdate']
            gallery_id = self.state['gallery_id']
            slider_id = self.state['slider_id']
        except:
            startdate = datetime.datetime.now().strftime('%Y%m%d')
            gallery_id = 0
            slider_id = -1
        if startdate == datetime.datetime.now().strftime('%Y%m%d') and slider_id == -1:
            # 1. Start überhaupt
            page = urllib.request.urlopen(START_URL).read()
            soup = bs4.BeautifulSoup(page, 'html.parser')
            _href = soup.find('a', {'class': 'mediaLink'})['href']
            match = re.search(r'.*blickpunkte-([0-9]{4})\.html', _href)
            gallery_id = match.group(1)
        elif startdate != datetime.datetime.now().strftime('%Y%m%d') and slider_id != -1:
            # 1. Start heute
            page = urllib.request.urlopen(START_URL).read()
            soup = bs4.BeautifulSoup(page, 'html.parser')
            _href = soup.find('a', {'class': 'mediaLink'})['href']
            match = re.search(r'.*blickpunkte-([0-9]{4})\.html', _href)
            gallery_id = match.group(1)
            slider_id = -1
        elif startdate == datetime.datetime.now().strftime('%Y%m%d') and slider_id != -1:
            # Weiterer Start heute
            pass
        else:
            # Weiterer Start
            gallery_id = self.state['lowest_gallery_id']
            gallery_id = int(gallery_id) - 2
            slider_id = -1

        while True:
            gallery_url = START_URL+'blickpunkte-'+str(gallery_id)+'.html'
            page = urllib.request.urlopen(gallery_url).read()
            soup = bs4.BeautifulSoup(page, 'html.parser')
            slider = soup.find('div', {'class': 'boxCon slider'})
            images = slider.findAll('img', {'class': 'img'})
            if int(slider_id) + 1 < len(images) :
                slider_id = int(slider_id) + 1
                image = images[slider_id]
                metadata = image['data-ctrl-attributeswap'].replace('\'', '"')
                metadata_json = json.loads(metadata)
                _href = metadata_json['action']['xl']['src'].replace('teaserM', 'videowebl')
                image_url = BASE_URL + _href
                try:
                    image_title = image['title']
                except:
                    image_title = ''
                next_image.image_name = image_url.split('/')[-1]
                next_image.source_url = urllib.parse.unquote(BASE_URL)
                next_image.source_type = DOWNLOADER_TYPE
                next_image.image_author = ''
                next_image.source_name = DOWNLOADER_DESCRIPTION
                next_image.image_url = urllib.parse.unquote(urllib.parse.urljoin(BASE_URL, image_url))
                next_image.location = ''
                next_image.keywords = image_title
                next_image.source_location = ''
                next_image.found_at_counter = last_image_counter + 1
                self.state['last_image_counter'] = next_image.found_at_counter
                self.state['startdate'] = startdate
                self.state['gallery_id'] = gallery_id
                self.state['slider_id'] = slider_id
                self.state['lowest_gallery_id'] = gallery_id
                return next_image
            else:
                gallery_id = self.state['lowest_gallery_id']
                gallery_id = int(gallery_id) - 2
                slider_id = -1
