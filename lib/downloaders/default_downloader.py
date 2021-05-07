#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Wariety - A wallpaper manager for MS Windows operating system.
#  Copyright (C) 2021 Roland Rickborn <wariety@gmx.net>
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

import abc
import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    import wariety.wariety as wariety
    import wariety_wallpaper
else:
    import wariety
    import lib.wariety_wallpaper as wariety_wallpaper


START_URL = ''
BASE_URL = ''
DOWNLOADER_TYPE = ''
DOWNLOADER_DESCRIPTION = ''
CAPABILITIES = {'single': 'single', 'many': 'many'}


class DefaultDownloader(abc.ABC):

    def __init__(self, config=None):
        """
        Create a downloader for an image source
        :param config: optional, see get_config()
        """
        super().__init__()
        logging.debug('__init__({})'.format(config))
        self.config = config
        self.target_folder = os.path.join(os.environ['LOCALAPPDATA'], wariety.APP_NAME)
        self.capability = CAPABILITIES['single']
        self.start_url = START_URL
        self.base_url = BASE_URL
        self.downloader_type = DOWNLOADER_TYPE
        self.downloader_desc = DOWNLOADER_DESCRIPTION
        self.next_image = wariety_wallpaper.WarietyWallpaper()
        self.proxies = {}
        if self.config.proxy_enable:
            self.proxies = self.get_proxy()

    def load_state(self, dl_typ):
        """
        Loads the state as json inside the downloader's target folder.
        :return:
        """

        logging.debug('load_state()')

        _state_filename = dl_typ+'.json'
        _state_file_folder = os.path.join(os.environ['LOCALAPPDATA'], wariety.APP_NAME)
        _state_file = os.path.join(_state_file_folder, _state_filename)
        if os.path.isfile(_state_file):
            with open(_state_file) as f:
                self.state = json.load(f)
        else:
            self.state = {}

    def save_state(self, dl_typ):
        """
        Persists the state as json inside the downloader's target folder. Prevents
        empty states.
        """

        logging.debug('save_state()')

        _state_filename = dl_typ + '.json'
        _state_file_folder = os.path.join(os.environ['LOCALAPPDATA'], wariety.APP_NAME)
        _state_file = os.path.join(_state_file_folder, _state_filename)
        if len(self.state) != 0:
            with open(_state_file, 'w') as f:
                json.dump(self.state, f)
        else:
            logging.debug('save_state() - update_download_folder was not called before save_state')

    def get_start_url(self):
        return self.start_url

    def get_proxy(self):
        _proxies = {}
        _proxies['http'] = '{}:{}'.format(self.config.proxy_address, self.config.proxy_port)
        _proxies['https'] = '{}:{}'.format(self.config.proxy_address, self.config.proxy_port)
        return _proxies

    @abc.abstractmethod
    def get_base_url(self):
        return self.base_url

    @abc.abstractmethod
    def get_next_image(self, last_image_counter=0):
        return self.next_image

    @abc.abstractmethod
    def get_downloader_type(self):
        return self.downloader_type

    @abc.abstractmethod
    def get_downloader_description(self):
        return self.downloader_desc

    @abc.abstractmethod
    def get_capability(self):
        return self.capability
