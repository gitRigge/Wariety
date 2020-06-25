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

file_content = """#!/usr/bin/env python
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

import logging
import sys

logger = logging.getLogger(__name__)
START_URL = ''
BASE_URL = 'zzz'
DOWNLOADER_TYPE = 'xxx'
DOWNLOADER_DESCRIPTION = 'yyy'
CAPABILITIES = {'single': 'single', 'many': 'many'}

if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


class www(DefaultDownloader):

    def __init__(self, config=None):
        self.config = config
        self._load_state(DOWNLOADER_TYPE)
        super().__init__(config)

    def __del__(self):
        self.save_state(DOWNLOADER_TYPE)

    def get_next_image(self, last_image_counter=0):
        next_image = None
        print(self.target_folder)
        return next_image

    def get_downloader_type(self):
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        return CAPABILITIES['single']

    def get_base_url(self):
        return BASE_URL
"""

for i in range(0, 20):
    print('i = {}'.format(i))
    new_file_name = 'test_downloader_'+str(i)+'.py'
    www = 'Test_'+str(i)+'_Downloader'
    xxx = 'test_'+str(i)
    yyy = 'This is my Test '+str(i)+' Downloader'
    zzz = 'https://start_scraping_from_'+str(i)+'.here'
    _file_content = file_content.replace('www', www).replace('xxx', xxx).replace('yyy', yyy).replace('zzz', zzz)
    f = open(new_file_name, 'w')
    f.write(_file_content)
    f.close()
