#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os

file_content = """#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

sys.path.insert(1, '../../lib')
from downloaders.default_downloader import DefaultDownloader

class www(DefaultDownloader):

    def get_next_image(self, last_image_counter=0):
        next_image = None
        print(self.target_folder)
        return next_image

    def get_downloader_type(self):
        return 'xxx'

    def get_downloader_description(self):
        return 'yyy'

    def get_capability(self):
        return self.capability

    def get_base_url(self):
        return 'zzz'
"""

for i in range(0, 20):
    print('i = {}'.format(i))
    new_file_name = 'testdownloader_'+str(i)+'.py'
    www = 'Test_'+str(i)+'_Downloader'
    xxx = 'test_'+str(i)
    yyy = 'This is my Test '+str(i)+' Downloader'
    zzz = 'https://start_scraping_from_'+str(i)+'.here'
    _file_content = file_content.replace('www', www).replace('xxx', xxx).replace('yyy', yyy).replace('zzz', zzz)
    f = open(new_file_name, 'w')
    f.write(_file_content)
    f.close()