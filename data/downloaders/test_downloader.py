#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import sys

logger = logging.getLogger(__name__)
START_URL = ''
BASE_URL = 'https://start_scraping_from.here'
DOWNLOADER_TYPE = 'test'
DOWNLOADER_DESCRIPTION = 'This is my Test Downloader'
CAPABILITIES = {'single': 'single', 'many': 'many'}

if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


class TestDownloader(DefaultDownloader):

    def __init__(self, config=None):
        self.config = config
        self._load_state(DOWNLOADER_TYPE)
        super().__init__(config)

    def __del__(self):
        self.save_state(DOWNLOADER_TYPE)

    def get_next_image(self, last_image_counter=0):
        next_image = wariety_wallpaper.WarietyWallpaper()
        print(self.target_folder)
        return None

    def get_downloader_type(self):
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        return CAPABILITIES['single']

    def get_base_url(self):
        return BASE_URL
