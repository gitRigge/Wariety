#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Wariety - A wallpaper manager for MS Windows operating system.
#  Copyright (C) 2024 Roland Rickborn <wariety@gmx.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see https://www.gnu.org/licenses/.

import datetime
import json
import locale
import logging
import sys
import urllib.parse

import requests

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


START_URL = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
BASE_URL = 'https://www.bing.com/'
DOWNLOADER_TYPE = 'bingarchive'
DOWNLOADER_DESCRIPTION = 'Bing Image Of The Day Archive'
CAPABILITIES = {'single': 'single', 'many': 'many'}


class BingArchiveDownloader(DefaultDownloader):

    def __init__(self, config=None):
        logging.debug('__init__(config)')
        self.config = config
        self.load_state(DOWNLOADER_TYPE)
        super().__init__(config)

    def __del__(self):
        logging.debug('__del__()')
        self.save_state(DOWNLOADER_TYPE)

    def get_downloader_type(self):
        logging.debug('get_downloader_type()')
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        logging.debug('get_downloader_description()')
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        logging.debug('get_capability()')
        return CAPABILITIES['single']

    def get_base_url(self):
        logging.debug('get_base_url()')
        return BASE_URL

    def get_calculated_idx(self):
        """
        Calculates the URL parameters based on the previously
        used parameters.
        :return ret_val:
        """

        logging.debug('get_calculated_idx()')

        ret_val = 0

        try:
            lastidx = self.state['idx']
            laststartdate = self.state['startdate']
        except:
            logging.debug('get_calculated_idx() - no state available')
            lastidx = 0
            laststartdate = datetime.datetime.now().strftime('%Y%m%d')

        locale.setlocale(locale.LC_TIME, "de_DE")
        now = datetime.datetime.now().strftime('%Y%m%d')
        now_dtime = datetime.datetime.strptime(now, '%Y%m%d')
        laststartdate_dtime = datetime.datetime.strptime(laststartdate, '%Y%m%d')
        diff = now_dtime - laststartdate_dtime
        ret_val = diff.days + lastidx + 1
        logging.debug('get_calculated_idx() - {}'.format(ret_val))
        return ret_val

    def get_next_image(self, last_image_counter=0):
        """
        Retrieves a BING picture of the day and returns it
        as an instance of wariety wallpaper. Depending on the counter
        given by 'last_image_counter' returns the next picture.
        :param last_image_counter:
        :return next_image:
        """

        logging.debug('get_next_image({})'.format(last_image_counter))

        # Generate empty image
        next_image = wariety_wallpaper.WarietyWallpaper()

        # Receive image data
        my_idx = self.get_calculated_idx()
        try:
            my_start_url = START_URL.replace('0', str(my_idx))
            session = requests.Session()
            session.proxies.update(self.proxies)
            headers = {
                'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/131.0.2903.86",
                'accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
                'referer': 'https://dont_worry.org',
            }
            response = session.get(my_start_url, stream=True, verify=False, headers=headers)
            image_data = json.loads(response.text)

            # Collect image data
            image_url = image_data["images"][0]["url"]
            image_url = image_url.split("&")[0]
            image_title = image_data["images"][0]["title"]
            image_copyright = image_data["images"][0]["copyright"]
            if image_title:
                image_title = image_title + '.'
            if image_copyright:
                image_copyright = image_copyright + '.'
            _next_image_url = urllib.parse.urljoin(BASE_URL, image_url)
            _next_image_url = _next_image_url.split('/')[-1].split('=')[-1]
            try:
                next_image.image_name = urllib.parse.unquote(_next_image_url)
            except:
                logging.debug('get_next_image() - invalid URL {}'.format(_next_image_url))
                next_image.image_name = ''

            # Fill image data
            next_image.source_url = urllib.parse.unquote(BASE_URL)
            next_image.source_type = DOWNLOADER_TYPE
            next_image.image_author = ''
            next_image.source_name = DOWNLOADER_DESCRIPTION
            next_image.image_url = urllib.parse.unquote(urllib.parse.urljoin(BASE_URL, image_url))
            next_image.location = ''
            next_image.keywords = '{0} {1}'.format(image_title, image_copyright).strip()
            next_image.source_location = ''
            next_image.found_at_counter = last_image_counter

            # Store state
            self.state['last_image_counter'] = next_image.found_at_counter
            startdate = datetime.datetime.now().strftime('%Y%m%d')
            self.state['startdate'] = startdate
            self.state['idx'] = my_idx

        except requests.ConnectionError:
            logging.debug('get_next_image() - ConnectionError')

        return next_image
