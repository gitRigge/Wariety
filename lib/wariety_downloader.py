#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import logging
import os
import PIL.Image
import random
import requests
import shutil
import struct
import sys
import time
import threading
import warnings
import win32api

sys.path.insert(1, '../lib')
sys.path.insert(1, '../lib/downloaders')
sys.path.insert(1, '../wariety')
import wariety_config
import wariety_database

logger = logging.getLogger(__name__)


class WarietyDownloader(threading.Thread):
    """docstring for WarietyDownloader"""

    def __init__(self, download_schedule=0, config={}):
        logger.debug('Starting downloader thread')
        logger.debug('__init__()')
        self.config = config
        self.enabled_sources = {}
        self.database = wariety_database.WarietyDatabase(self.config)
        # Initial dl size check
        self.start_check_download_folder_size()
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self.down_sched = int(download_schedule)
        self.seconds_until_fire = 60 * int(download_schedule)
        self.check_interval = 1
        self.keep_running = True
        if int(download_schedule) == 0:
            self.do_downloads = False
        else:
            self.do_downloads = True
        self.start()

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping downloader thread')
        pass

    def run(self):
        """Run Worker Thread."""
        logger.debug('run()')
        while self.keep_running:
            self.seconds_until_fire = self.seconds_until_fire - self.check_interval
            if self.seconds_until_fire == 0:
                self.seconds_until_fire = 60 * self.down_sched
                self.start_new_wallpaper_download()
                # check dl size after each download
                self.start_check_download_folder_size()
            else:
                time.sleep(self.check_interval)

    def stop(self):
        logger.debug('stop()')
        self.seconds_until_fire = 1
        self.keep_running = False

    def start_new_wallpaper_download(self):
        logger.debug('start_new_wallpaper_download()')
        my_downloader = self.get_random_downloader()
        my_downloader_type = my_downloader.get_downloader_type()
        my_downloader_capability = my_downloader.get_capability()
        my_image = self.database.get_latest_image(source_type=my_downloader_type)
        if my_downloader_capability == 'many':
            # Get new full image urls until one is not yet in DB
            while self.database.exists_image_by_url_or_path(my_image.image_url) or my_image.image_url == '':
                my_get_counter = my_image.found_at_counter + 1
                my_image = my_downloader.get_next_image(my_get_counter)
            # Check image name
            if my_image.image_name == '':
                my_image.image_name = self.get_generated_image_name(my_image.image_url)
            # Download image
            my_image.image_path = self.download_image(my_image.image_url, my_image.image_name)
            my_image.image_md5_hash = self.database.get_md5_hash_of_file(my_image.image_path)
            # Turn of PIL DecompressionBombWarning
            warnings.simplefilter('ignore', PIL.Image.DecompressionBombWarning)
            if self.database.is_image_landscape(my_image.image_path):
                my_image.image_orientation = my_image.wallpaper_orientations['landscape']
            else:
                my_image.image_orientation = my_image.wallpaper_orientations['portrait']
            self.database.add_image_to_database(my_image)
            self.resize_image(my_image.image_path)
        elif my_downloader_capability == 'single':
            my_get_counter = my_image.found_at_counter + 1
            my_image = my_downloader.get_next_image(my_get_counter)
            if not self.database.exists_image_by_url_or_path(my_image.image_url):
                # Check image name
                if my_image.image_name == '':
                    my_image.image_name = self.get_generated_image_name(my_image.image_url)
                # Download image
                my_image.image_path = self.download_image(my_image.image_url, my_image.image_name)
                my_image.image_md5_hash = self.database.get_md5_hash_of_file(my_image.image_path)
                # Turn of PIL DecompressionBombWarning
                warnings.simplefilter('ignore', PIL.Image.DecompressionBombWarning)
                if self.database.is_image_landscape(my_image.image_path) is True:
                    my_image.image_orientation = my_image.wallpaper_orientations['landscape']
                else:
                    my_image.image_orientation = my_image.wallpaper_orientations['portrait']
                self.database.add_image_to_database(my_image)
                self.resize_image(my_image.image_path)

    def get_enabled_sources(self):
        logger.debug('get_enabled_sources()')
        for key, value in self.config.items():
            if key.startswith('source_') and value is True:
                built_in_downloaders = wariety_config.BUILT_IN_DOWNLOADERS
                if key in built_in_downloaders:
                    self.enabled_sources[key] = built_in_downloaders[key]
                else:
                    self.enabled_sources[key] = ''
        return self.enabled_sources

    def get_random_downloader(self):
        logger.debug('get_random_downloader()')
        try:
            sys.path.append(r'lib\downloaders')
            enabled_sources = self.get_enabled_sources()
            my_downloader = __import__(random.choice(list(enabled_sources.values())))
            return my_downloader
        except IndexError:
            return ''

    def download_image(self, full_image_url, image_name):
        """Creates the folder 'WarietyWallpaperImages' in the temporary
        location if it does not yet exist. Downloads the image given
        by 'full_image_url', stores it there and returns the path to it
        """
        logger.debug('download_image({}, {})'.format(full_image_url, image_name))
        dir_path = self.config['download_wallpaper_folder']
        os.makedirs(dir_path, exist_ok=True)
        if os.path.isfile(full_image_url):
            im = PIL.Image.open(full_image_url)
            image_name = '{0}.{1}'.format(image_name, im.format.lower())
            shutil.copyfile(full_image_url, os.path.join(dir_path, image_name))
        else:
            img_data = requests.get(full_image_url).content
            with open(os.path.join(dir_path, image_name), 'wb') as handler:
                handler.write(img_data)
        return os.path.join(dir_path, image_name)

    def resize_image(self, full_image_path):
        """Checks image size and resolution of image given by 'full_image_path'
        and compares it with screen size and resolution. Resizes image if necessary
        and overwrites image then.
        """
        logger.debug('resize_image({})'.format(full_image_path))
        image = PIL.Image.open(full_image_path)
        image_width = image.size[0]
        image_heigth = image.size[1]
        screen_width = self.get_screen_width()
        screen_height = self.get_screen_height()
        new_size = self.get_correct_image_size(image_width, image_heigth, screen_width, screen_height)
        new_image = image.resize(new_size, PIL.Image.LANCZOS)
        new_image.save(full_image_path, dpi=(72, 72))

    def get_generated_image_name(self, full_image_url):
        """Expects URL to an image, retrieves its file extension and returns
        an image name based on the current date and with the correct file
        extension
        """
        logger.debug('get_generated_image_name({})'.format(full_image_url))
        image_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        image_extension = full_image_url.split(".")[-1]
        image_name = image_name + "." + image_extension
        return image_name

    def is_screen_landscape(self):
        """Checks the current screen orientation and returns 'True' if the screen orientation
        is landscape
        """
        logger.debug('is_screen_landscape()')
        if self.get_screen_width() / self.get_screen_height() > 1:
            return True
        else:
            return False

    def get_screen_width(self):
        """Reads Windows System Metrics and returns screen width in pixel"""
        logger.debug('get_screen_width()')
        width = win32api.GetSystemMetrics(0)
        return width

    def get_screen_height(self):
        """Reads Windows System Metrics and returns screen heigth in pixel"""
        logger.debug('get_screen_height()')
        height = win32api.GetSystemMetrics(1)
        return height

    def get_correct_image_size(self, image_width, image_heigth, screen_width, screen_height):
        """Calculates the correct proportional image size depending
        on the current image width and height and on the screen's width
        and height. Returns a tuple of width and height.
        """
        logger.debug(
            'get_correct_image_size({}, {}, {}, {})'.format(image_width, image_heigth, screen_width, screen_height))
        new_width = 0
        new_height = 0
        if (image_width / image_heigth) >= 1:
            new_width = screen_width
            new_height = int((image_heigth / image_width) * screen_width)
        else:
            new_height = screen_height
            new_width = int((image_width / image_heigth) * screen_height)
        return (new_width, new_height)

    def start_check_download_folder_size(self):
        """
        Reads download folder settings (path, max size), calculates limit and removes
        images if limit is reached. In case of deletion, it deletes the oldest images first.
        :return:
        """
        logger.debug('start_check_download_folder_size()')
        download_folder_path = self.config['download_wallpaper_folder']
        check_download_folder_size = self.config['max_wallpaper_folder']
        download_folder_max_size = self.config['max_wallpaper_folder_size']
        limit = int(download_folder_max_size) * 1000 * 1000
        if check_download_folder_size:
            # Clear folder
            while self.get_download_folder_size(download_folder_path) >= limit:
                my_image = self.database.get_oldest_image()
                self.database.remove_image_by_id(my_image.id)
                try:
                    self.database.remove_image_file(my_image.image_path)
                except PermissionError:
                    logger.debug('start_check_download_folder_size() - PermissionError')
                except:
                    e = sys.exc_info()[0]
                    logger.debug('start_check_download_folder_size() - {}'.format(e))
                time.sleep(1)

    def get_download_folder_size(self, start_path='.'):
        """
        Tries to read the folder size of the folder given by 'start_path'.
        Returns total folder size.
        :param start_path:
        :return total_size:
        """
        logger.debug('get_download_folder_size({})'.format(start_path))

        # Default value
        total_size = 0

        try:
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except:
            e = sys.exc_info()[0]
            logger.debug('get_download_folder_size() - {}'.format(e))

        finally:
            return total_size
