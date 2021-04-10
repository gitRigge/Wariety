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

import glob
import imghdr
import logging
import os
import sys

logger = logging.getLogger(__name__)
if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


START_URL = 'http://...'
BASE_URL = r'%LOCALAPPDATA%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
DOWNLOADER_TYPE = 'spotlight'
DOWNLOADER_DESCRIPTION = 'Microsoft Spotlight'
CAPABILITIES = {'single': 'single', 'many': 'many'}


class SpotlightDownloader(DefaultDownloader):

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
        """Loops through all locally stored Windows Spotlight assets
        and copies and returns the latest asset which has the same orientation as the screen
        """
        next_image = wariety_wallpaper.WarietyWallpaper()
        counter = -1
        localappdata = os.environ['LOCALAPPDATA']
        localstate_assests = r'\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
        list_of_files = sorted(glob.glob(localappdata+localstate_assests+'\*'), key=os.path.getmtime, reverse=True)
        for asset in list_of_files:
            counter = counter + 1
            if counter == last_image_counter:
                extension = imghdr.what(asset)
                if extension in ['jpeg', 'jpg', 'png']:
                    # Generate pseudo url
                    try:
                        next_image.image_name = os.path.split(asset)[1].split('\\')[-1]
                    except:
                        next_image.image_name = ''
                    next_image.source_url = 'https://docs.microsoft.com/en-us/windows/configuration/windows-spotlight'
                    next_image.source_type = DOWNLOADER_TYPE
                    next_image.source_name = 'Microsoft Spotlight'
                    next_image.image_url = asset
                    next_image.found_at_counter = last_image_counter + 1
                    return next_image