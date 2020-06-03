#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import configparser
import logging
import os
import winreg
import sys
from pubsub import pub

logger = logging.getLogger(__name__)

BUILT_IN_DOWNLOADERS = {
    'source_windows_spotlight':'microsoft_spotlight',
    'source_flickr_peter_levi':'peter_levys_flickr_collection',
    'source_bing':'bing_image_of_the_day',
    'source_wikimedia':'wikimedia_picture_of_the_day'
    }

class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return winreg.ExpandEnvironmentStrings(value.replace("'",""))

class WarietyConfig(object):
    """docstring for WarietyConfig"""
    
    def __init__(self, config_file):
        logger.debug('Starting config')
        logger.debug('__init__({})'.format(config_file))
        # General
        self.start_at_startup = False
        self.wallpaper_change = False
        self.wallpaper_change_interval = 8
        self.change_wallpaper_at_startup = False
        self.download_wallpaper = False
        self.download_wallpaper_interval = 8
        self.download_wallpaper_folder = r'%LOCALAPPDATA%\Wariety\Downloaded'
        self.max_wallpaper_folder = False
        self.max_wallpaper_folder_size = 128
        self.manual_download = False
        self.manual_download_folder = r'%LOCALAPPDATA%\Wariety\Fetched'
        self.animate_system_tray_icon = False
        self.show_balloon_message = False

        # Sources
        self.source_windows_spotlight = True
        self.source_flickr_peter_levi = True
        self.source_bing = True
        self.source_wikimedia = True
        self.source_manual = True
        self.config = configparser.ConfigParser(interpolation=EnvInterpolation())
        self.config_file = config_file

        # Read
        self.read_config_file()
        self.read_config()

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping config')

    def on_close(self):
        """Update, push and write config
        """
        logger.debug('on_close()')
        self.set_config()
        self.push_updated_config()
        self.write_config_file()

    def read_config_file(self):
        logger.debug('read_config_file()')
        if os.path.isfile(self.config_file):
            self.config.read(self.config_file)

    def write_config_file(self):
        logger.debug('write_config_file()')
        if os.path.isfile(self.config_file):
            with open(self.config_file, 'w') as config_file:
                self.config.write(config_file)

    def read_config(self):
        logger.debug('read_config()')
        # General
        self.start_at_startup = self.config['General'].getboolean('start_at_startup')
        self.wallpaper_change = self.config['General'].getboolean('wallpaper_change')
        self.wallpaper_change_interval = self.config['General'].getint('wallpaper_change_interval')
        self.change_wallpaper_at_startup = self.config['General'].getboolean('change_wallpaper_at_startup')
        self.download_wallpaper = self.config['General'].getboolean('download_wallpaper')
        self.download_wallpaper_interval = self.config['General'].getint('download_wallpaper_interval')
        self.download_wallpaper_folder = self.config['General'].get('download_wallpaper_folder', r'%LOCALAPPDATA%\Wariety\Downloaded')
        self.max_wallpaper_folder = self.config['General'].getboolean('max_wallpaper_folder')
        self.max_wallpaper_folder_size = self.config['General'].getint('max_wallpaper_folder_size')
        self.manual_download = self.config['General'].getboolean('manual_download')
        self.manual_download_folder = self.config['General'].get('manual_download_folder')
        self.animate_system_tray_icon = self.config['General'].getboolean('animate_system_tray_icon')
        self.show_balloon_message = self.config['General'].getboolean('show_balloon_message')

        # Sources
        self.source_windows_spotlight = self.config['Sources'].getboolean('source_windows_spotlight')
        self.source_flickr_peter_levi = self.config['Sources'].getboolean('source_flickr_peter_levi')
        self.source_bing = self.config['Sources'].getboolean('source_bing')
        self.source_wikimedia = self.config['Sources'].getboolean('source_wikimedia')
        self.source_manual = self.config['Sources'].getboolean('source_manual')

    def set_config(self):
        logger.debug('set_config()')
        # General
        self.config.set('General', 'start_at_startup', str(self.start_at_startup))
        self.config.set('General', 'wallpaper_change', str(self.wallpaper_change))
        self.config.set('General', 'wallpaper_change_interval', str(self.wallpaper_change_interval))
        self.config.set('General', 'change_wallpaper_at_startup', str(self.change_wallpaper_at_startup))
        self.config.set('General', 'download_wallpaper', str(self.download_wallpaper))
        self.config.set('General', 'download_wallpaper_interval', str(self.download_wallpaper_interval))
        self.config.set('General', 'download_wallpaper_folder', str(self.download_wallpaper_folder))
        self.config.set('General', 'max_wallpaper_folder', str(self.max_wallpaper_folder))
        self.config.set('General', 'max_wallpaper_folder_size', str(self.max_wallpaper_folder_size))
        self.config.set('General', 'manual_download', str(self.manual_download))
        self.config.set('General', 'manual_download_folder', str(self.manual_download_folder))
        self.config.set('General', 'animate_system_tray_icon', str(self.animate_system_tray_icon))
        self.config.set('General', 'show_balloon_message', str(self.show_balloon_message))

        # Sources
        self.config.set('Sources', 'source_windows_spotlight', str(self.source_windows_spotlight))
        self.config.set('Sources', 'source_flickr_peter_levi', str(self.source_flickr_peter_levi))
        self.config.set('Sources', 'source_bing', str(self.source_bing))
        self.config.set('Sources', 'source_wikimedia', str(self.source_wikimedia))
        self.config.set('Sources', 'source_manual', str(self.source_manual))

    def push_updated_config(self):
        logger.debug('push_updated_config()')
        pub.sendMessage("config updated", msg=self.to_dict())

    def to_dict(self):
        logger.debug('to_dict()')
        my_config = {
            'start_at_startup':self.start_at_startup,
            'wallpaper_change':self.wallpaper_change,
            'wallpaper_change_interval':self.wallpaper_change_interval,
            'change_wallpaper_at_startup':self.change_wallpaper_at_startup,
            'download_wallpaper':self.download_wallpaper,
            'download_wallpaper_interval':self.download_wallpaper_interval,
            'download_wallpaper_folder':self.download_wallpaper_folder,
            'max_wallpaper_folder':self.max_wallpaper_folder,
            'max_wallpaper_folder_size':self.max_wallpaper_folder_size,
            'manual_download':self.manual_download,
            'manual_download_folder':self.manual_download_folder,
            'animate_system_tray_icon':self.animate_system_tray_icon,
            'show_balloon_message':self.show_balloon_message,
            'source_windows_spotlight':self.source_windows_spotlight,
            'source_flickr_peter_levi':self.source_flickr_peter_levi,
            'source_bing':self.source_bing,
            'source_wikimedia':self.source_wikimedia,
            'source_manual':self.source_manual
        }
        return my_config