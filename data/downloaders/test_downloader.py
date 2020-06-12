#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import sys

logger = logging.getLogger(__name__)
if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


class TestDownloader(DefaultDownloader):

    def get_next_image(self, last_image_counter=0):
        next_image = wariety_wallpaper.WarietyWallpaper()
        print(self.target_folder)
        return None

    def get_downloader_type(self):
        return 'test'

    def get_downloader_description(self):
        return 'This is my Test Downloader'

    def get_capability(self):
        return self.capability

    def get_base_url(self):
        return 'https://start_scraping_from.here'
