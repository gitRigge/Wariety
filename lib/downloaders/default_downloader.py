#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import abc
import logging
import json
import os
import sys

sys.path.insert(1, '../lib')
import wariety_wallpaper

START_URL = ''
BASE_URL = ''
DOWNLOADER_TYPE = ''
DOWNLOADER_DESCRIPTION = ''
CAPABILITIES = {'single': 'single', 'many': 'many'}

logger = logging.getLogger(__name__)

class DefaultDownloader(abc.ABC):
    def __init__(self, config=None, capability='single'):
        """
        Create a downloader for an image source
        :param config: optional, see get_config()
        """
        super().__init__()
        self.config = config
        self.target_folder = os.path.join(os.environ['LOCALAPPDATA'],'Wariety')  # TODO Replace static string 'Wariety'
        self.state = None
        if capability in CAPABILITIES:
            self.capability = capability
        else:
            self.capability = 'single'
        self.start_url = START_URL
        self.base_url = BASE_URL
        self.downloader_type = DOWNLOADER_TYPE
        self.downloader_desc = DOWNLOADER_DESCRIPTION
        self.next_image = wariety_wallpaper.WarietyWallpaper()
        self._downloader_id = os.path.basename(__file__)

    def _load_state(self):
        try:
            with open(os.path.join(self.target_folder, self._downloader_id+'.json')) as f:
                self.state = json.load(f)
        except Exception:
            self.state = {}

    def save_state(self):
        """
        Persists the state as json inside the downloader's target folder.
        state is a dict that is used internally by Variety, but the downloaders can also use it
        keeping any sort of state is necessary for the downloader.
        """
        if self.target_folder is None:
            raise Exception("update_download_folder was not called before save_state")
        with open(os.path.join(self.target_folder, self._downloader_id+'.json'), 'w') as f:
            json.dump(self.state, f)

    def get_start_url(self):
        return self.start_url

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
