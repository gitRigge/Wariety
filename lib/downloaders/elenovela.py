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


START_URL = 'https://www.flickr.com/photos/elenovela/'
BASE_URL = 'https://www.flickr.com/photos/elenovela/'
DOWNLOADER_TYPE = 'elenovela'
DOWNLOADER_DESCRIPTION = 'Elenovela\'s Flickr Collection'
CAPABILITIES = {'single': 'single', 'many': 'many'}

API_KEY = u'2861cd9d551ee36dc08123f5c7c04ff6'
USER_ID = '90101761@N05'


class ElenovelaDownloader(DefaultDownloader):

    def __init__(self, config=None):
        logging.debug('__init__(config) - {}'.format(DOWNLOADER_TYPE))
        self.config = config
        self.load_state(DOWNLOADER_TYPE)
        super().__init__(config)

    def __del__(self):
        logging.debug('__del__() - {}'.format(DOWNLOADER_TYPE))
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

    def retrieve_images_data(self, page=1):
        """
        Calls the Flickr API 'flickr.photos.search', retrieves and returns
        as JSON up to 500 datasets of images. 'page' specifies the page of
        results to return. If this argument is omitted, it defaults to 1.
        Returns fail in case of errors.
        :return ret_val:
        """

        logging.debug('retrieve_image_data_once({})'.format(page))

        # Return value
        ret_val = {'stat': 'fail'}

        url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={}&user_id={}&per_page=500&page={}&content_type=1&format=json&nojsoncallback=1'.format(API_KEY, USER_ID, page)
        session = requests.Session()
        session.proxies.update(self.proxies)
        verifySsl = True
        if self.config.proxy_enable:
            verifySsl = False
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/131.0.2903.86",
            'accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
            'referer': 'https://dont_worry.org',
        }
        try:
            response = session.get(url, stream=True, verify=verifySsl, headers=headers)
            ret_val = json.loads(response.text)
        except Exception as e:
            logging.debug('retrieve_image_data_once() - ConnectionError', e)

        return ret_val

    def retrieve_image_info_data(self, image_id, image_secret):
        """
        Calls the Flickr API 'flickr.photos.getInfo', retrieves and returns
        as JSON the info details of the image specified by 'image_id'.
        Returns fail in case of errors.
        """

        logging.debug('retrieve_image_detail_data({}, {})'.format(image_id, image_secret))

        # Return value
        ret_val = {'stat': 'fail'}

        url = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key={}&photo_id={}&secret={}&format=json&nojsoncallback=1'.format(API_KEY, image_id, image_secret)
        session = requests.Session()
        session.proxies.update(self.proxies)
        verifySsl = True
        if self.config.proxy_enable:
            verifySsl = False
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/131.0.2903.86",
            'accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
            'referer': 'https://dont_worry.org',
        }
        try:
            response = session.get(url, stream=True, verify=verifySsl, headers=headers)
            ret_val = json.loads(response.text)
        except Exception as e:
            logging.debug('retrieve_image_detail_data() - ConnectionError', e)

        return ret_val

    def retrieve_image_sizes_data(self, image_id):
        """
        Calls the Flickr API 'flickr.photos.getSizes', retrieves and returns
        as JSON the sizes of the image specified by 'image_id'.
        Returns fail in case of errors.
        :return:
        """
        logging.debug('retrieve_image_sizes_data_and_get_url({})'.format(image_id))

        # Return value
        ret_val = {'stat': 'fail'}

        url = 'https://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={}&photo_id={}&format=json&nojsoncallback=1'.format(API_KEY, image_id)
        session = requests.Session()
        session.proxies.update(self.proxies)
        verifySsl = True
        if self.config.proxy_enable:
            verifySsl = False
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/131.0.2903.86",
            'accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
            'referer': 'https://dont_worry.org',
        }
        try:
            response = session.get(url, stream=True, verify=verifySsl, headers=headers)
            ret_val = json.loads(response.text)
        except Exception as e:
            logging.debug('retrieve_image_sizes_data_and_get_url() - ConnectionError', e)

        return ret_val

    def get_next_image(self, last_image_counter=0):
        """Retrieves the URL of the latest image of Elenovela's Flickr Collection,
        downloads the image, stores it in a temporary folder and returns the path
        to it
        """

        logging.debug('get_next_image({})'.format(last_image_counter))

        # Generate empty image
        next_image = wariety_wallpaper.WarietyWallpaper()
        page = 0

        if len(self.state) == 0:
            self.state = self.retrieve_images_data()
            self.state['page'] = 1
        else:
            page = self.state['page']

        # get image url
        if self.state['stat'] == 'ok':
            if last_image_counter >= len(self.state['photos']['photo']):
                self.state = self.retrieve_images_data(int(page) + 1)
            image_id = self.state['photos']['photo'][last_image_counter]['id']
            image_secret = self.state['photos']['photo'][last_image_counter]['secret']
            image_title = self.state['photos']['photo'][last_image_counter]['title']
            image_info_data = self.retrieve_image_info_data(image_id, image_secret)
            if image_info_data['stat'] == 'ok':
                image_sizes = self.retrieve_image_sizes_data(image_id)
                if image_sizes['stat'] == 'ok':
                    image_url = ''
                    for size in image_sizes['sizes']['size']:
                        if size['width'] > 1900:  # TODO get current system's screen sizes
                            image_url = size['source']
                            break

                    # Fill image data
                    next_image.source_url = urllib.parse.unquote(BASE_URL)
                    next_image.source_type = DOWNLOADER_TYPE
                    next_image.image_author = 'Elenovela'
                    next_image.source_name = DOWNLOADER_DESCRIPTION
                    next_image.image_url = urllib.parse.unquote(urllib.parse.urljoin(BASE_URL, image_url))
                    next_image.location = ''
                    next_image.keywords = image_title
                    next_image.source_location = ''
                    next_image.found_at_counter = last_image_counter

                    # Store state
                    self.state['last_image_counter'] = next_image.found_at_counter
                    startdate = datetime.datetime.now().strftime('%Y%m%d')
                    self.state['startdate'] = startdate
                    self.state['page'] = page

        return next_image
