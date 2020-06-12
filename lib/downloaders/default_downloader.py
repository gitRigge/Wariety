#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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
PROXIES = {'http': '', 'https': ''}


def set_proxy_with_environment_variable():
    """
    Sets HTTP and HTTPS proxies according to environment variables, if available.
    :return:
    """
    logging.debug('set_proxy_with_environment_variable()')

    PROXIES['http'] = os.getenv('HTTP_PROXY', False)
    PROXIES['https'] = os.getenv('HTTPS_PROXY', False)


class DefaultDownloader(abc.ABC):

    def __init__(self, config=None):
        """
        Create a downloader for an image source
        :param config: optional, see get_config()
        """
        super().__init__()
        logging.debug('__init__({})'.format(config))
        self.config = config
        _app_name = wariety.APP_NAME
        self.target_folder = os.path.join(os.environ['LOCALAPPDATA'], _app_name)
        self.state = {}
        self.use_proxy = False
        self.capability = CAPABILITIES['single']
        self.start_url = START_URL
        self.base_url = BASE_URL
        self.downloader_type = DOWNLOADER_TYPE
        self.downloader_desc = DOWNLOADER_DESCRIPTION
        set_proxy_with_environment_variable()
        if PROXIES['http']:
            self.with_http_proxy = True
        else:
            self.with_http_proxy = False
        if PROXIES['https']:
            self.with_https_proxy = True
        else:
            self.with_https_proxy = False
        self.next_image = wariety_wallpaper.WarietyWallpaper()

    def _load_state(self, dl_typ):
        """
        Loads the state as json inside the downloader's target folder.
        :return:
        """
        logging.debug('_load_state()')
        try:
            with open(os.path.join(self.target_folder, dl_typ+'.json')) as f:
                self.state = json.load(f)
        except Exception:
            self.state = {}

    def save_state(self, dl_typ):
        """
        Persists the state as json inside the downloader's target folder.
        """
        logging.debug('_load_state()')
        if self.target_folder is None:
            raise Exception("update_download_folder was not called before save_state")
        with open(os.path.join(self.target_folder, dl_typ+'.json'), 'w') as f:
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
