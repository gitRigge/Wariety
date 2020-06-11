#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

sys.path.insert(1, '../../lib')
from downloaders.default_downloader import DefaultDownloader

class Test_9_Downloader(DefaultDownloader):

    def get_next_image(self, last_image_counter=0):
        next_image = None
        print(self.target_folder)
        return next_image

    def get_downloader_type(self):
        return 'test_9'

    def get_downloader_description(self):
        return 'This is my Test 9 Downloader'

    def get_capability(self):
        return self.capability

    def get_base_url(self):
        return 'https://start_scraping_from_9.here'
