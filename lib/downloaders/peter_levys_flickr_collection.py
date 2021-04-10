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

import logging
import re
import sys

import requests

logger = logging.getLogger(__name__)
if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


START_URL = 'http://...'
BASE_URL = 'https://www.flickr.com/photos/peter-levi/'
DOWNLOADER_TYPE = 'peterlevi'
DOWNLOADER_DESCRIPTION = 'Peter Levi\'s Flickr Collection'
CAPABILITIES = {'single': 'single', 'many': 'many'}


class PeterLeviDownloader(DefaultDownloader):

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
        return CAPABILITIES['single']

    def get_base_url(self):
        return BASE_URL

    def get_next_image(self, last_image_counter=0):
        """Retrieves the URL of the latest image of Peter Levi's Flickr Collection,
        downloads the image, stores it in a temporary folder and returns the path
        to it
        """
        next_image = wariety_wallpaper.WarietyWallpaper()
        # get image url
        response = requests.get("https://www.flickr.com/photos/peter-levi/")
        match = re.search('([0-9]{10})_.*\.jpg\)', response.text)
        image_id = match.group(1)
        image_url = "https://www.flickr.com/photos/peter-levi/"+image_id+"/sizes/h/"
        response = requests.get(image_url)
        pattern = 'http.*'+image_id+'.*_h\.jpg'
        match = re.search(pattern, response.text)
        full_image_url = match.group(0)
        return next_image

        # # image's name
        # image_name = next_image.getGeneratedImageName(full_image_url)
        #
        # # Check and maintain DB
        # if not existsImageInDatabase(full_image_url):
        #     addImageToDatabase(full_image_url, image_name, "flickr")
        #     # download and save image
        #     full_image_path = downloadImage(full_image_url, image_name)
        #     updateImageInDatabase(full_image_url, full_image_path)
        # else:
        #     full_image_path = getImagePathFromDatabase(full_image_url)
        #
        # # Return full path to image
        # return full_image_path