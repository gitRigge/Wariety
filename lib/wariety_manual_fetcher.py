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

import datetime
import logging
import os
import sys
import time
import warnings

import PIL.Image
from PIL import IptcImagePlugin
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import wariety_database

logger = logging.getLogger(__name__)

class WarietyManualFetchHandler(FileSystemEventHandler):
    """Watchdog Event Handler"""

    def __init__(self, config={}):
        logger.debug('Starting manual fetch handler')
        logger.debug('__init__()')
        self.config = config
        self.database = wariety_database.WarietyDatabase(self.config)

    def on_created(self, event):
        """
        This method checks if the created file is an image file. If so,
        it checks whether the image exists in the database. If it does not,
        it adds the created image. Otherwise, it does nothing.
        :param event:
        :return:
        """
        logger.debug('on_created()')
        full_image_path = event.src_path
        if self.is_image_file(full_image_path) is True:
            if self.database.exists_image_by_url_or_path(full_image_path) == 0:
                logger.debug('on_created() - add new image')
                my_new_wallpaper = wariety_database.get_empty_image()
                self.fill_image_metadata(full_image_path, my_new_wallpaper)
                self.database.add_image_to_database(my_new_wallpaper)
            else:
                logger.debug('on_created() - image already exists. Do nothing')
        else:
            # Modified file is no image file - do nothing.
            logger.debug('on_created() - no image file. Do nothing.')

    def on_deleted(self, event):
        """
        This method checks whether the deleted file exists as image in the
        database. If so, it sets that image to status 'DELETED'.
        :param event:
        :return:
        """
        logger.debug('on_deleted()')
        full_image_path = event.src_path
        if self.database.exists_image_by_url_or_path(full_image_path):
            logger.debug('on_deleted() - remove image from DB.')
            self.database.remove_image_by_id(self.database.exists_image_by_url_or_path(full_image_path))
        else:
            logger.debug('on_deleted() - image is not in DB.')

    def on_moved(self, event):
        """
        This method checks if the moved file is an image file. If so,
        it checks whether the image exists in the database. If it does,
        it updates the database.
        :param event:
        :return:
        """
        logger.debug('on_moved()')
        full_image_path_old = event.src_path
        full_image_path = event.dest_path
        if self.is_image_file(full_image_path) is True:
            if self.database.exists_image_by_url_or_path(full_image_path_old):
                logger.debug('on_moved() - remove existing image')
                self.database.remove_image_by_id(self.database.exists_image_by_url_or_path(full_image_path_old))
                logger.debug('on_moved() - add moved image')
                my_new_wallpaper = wariety_database.get_empty_image()
                self.fill_image_metadata(full_image_path, my_new_wallpaper)
                self.database.add_image_to_database(my_new_wallpaper)
            else:
                logger.debug('on_moved() - add new image')
                my_new_wallpaper = wariety_database.get_empty_image()
                self.fill_image_metadata(full_image_path, my_new_wallpaper)
                self.database.add_image_to_database(my_new_wallpaper)
        else:
            # Modified file is no image file - do nothing.
            logger.debug('on_moved() - no image file. Do nothing.')

    def is_image_file(self, filename):
        """
        Checks whether the file given by 'filename' is a valid image format.
        If so, returns 'True'. Otherwise, returns 'False'.
        :param filename:
        :return is_image:
        """
        logger.debug('is_image_file()')

        # Turn of PIL DecompressionBombWarning
        warnings.simplefilter('ignore', PIL.Image.DecompressionBombWarning)

        is_image = False

        try:
            time.sleep(1)
            im = PIL.Image.open(filename)
            is_image = True
            im.close()
        except:
            e = sys.exc_info()[0]
            logger.debug('is_image_file() - {}'.format(e))

        logger.debug('is_image_file() returns {}'.format(str(is_image)))
        return is_image

    def fill_image_metadata(self, image_file_path, wallpaper):
        """
        Tries to read IPTC metadata from image given by 'image_file_path' and
        fills wallpaper object given by 'wallpaper' with the found IPTC metadata.
        If no IPTC metddata was found, fills default values.
        :param image_file_path:
        :param wallpaper:
        :return:
        """
        logger.debug('fill_image_metadata()')
        my_iptc = self.get_iptc_metadata(image_file_path)
        _i_name = self.get_image_name_by_metadata(my_iptc)
        if _i_name == '':
            wallpaper.image_name = str(os.path.basename(image_file_path))
        else:
            wallpaper.image_name = _i_name
        wallpaper.image_md5_hash = wariety_database.get_md5_hash_of_file(image_file_path)
        wallpaper.image_path = image_file_path
        wallpaper.source_url = '' # TODO
        wallpaper.source_type = 'fetched'
        wallpaper.image_author = self.get_image_author_by_metadata(my_iptc)
        wallpaper.image_url = image_file_path
        wallpaper.location = self.get_image_location_by_metadata(my_iptc)
        _s_name = self.get_image_source_name_by_metadata(my_iptc)
        if _s_name == '':
            wallpaper.source_name = 'Fetched Folder'
        else:
            wallpaper.source_name = _s_name
        wallpaper.keywords = self.get_image_keywords_by_metadata(my_iptc)
        wallpaper.found_at_counter = 0
        if wariety_database.is_image_landscape(image_file_path) is True:
            wallpaper.image_orientation = wallpaper.wallpaper_orientations['landscape']
        else:
            wallpaper.image_orientation = wallpaper.wallpaper_orientations['portrait']
        dl_date = datetime.datetime.now()
        wallpaper.download_date = dl_date.strftime("%Y%m%d%H%M%S")
        wallpaper.status = wallpaper.wallpaper_statuses['DOWNLOADED']

    def get_iptc_metadata(self, image_file_path):
        """
        Reads the IPTC metadata of an image given by 'image_file_path' and returns it.
        Returns empty array if IPTC metadata is not available.
        :param image_file_path:
        :return iptc:
        """

        logger.debug('get_iptc_metadata()')

        try:
            im = PIL.Image.open(image_file_path)
            iptc = IptcImagePlugin.getiptcinfo(im)
            im.close()
            if not iptc is None:
                return iptc
            else:
                return []
        except:
            e = sys.exc_info()[0]
            logger.debug('is_image_landscape() - {}'.format(e))

    def get_image_name_by_metadata(self, iptc):
        """
        Tries to find either a headline or a document title in provided IPTC
        metadata given by 'iptc'. Returns empty string if nothing is found.
        :param iptc:
        :return image_name:
        """
        logger.debug('get_image_name_by_metadata()')
        image_name = ''

        if (2, 105) in iptc:
            # we have a headline
            image_name = iptc[(2, 105)].decode('UTF-8')
        elif (2, 5) in iptc:
            # we have a document title
            image_name = iptc[(2, 5)].decode('UTF-8')
        else:
            image_name = ''

        return image_name

    def get_image_source_name_by_metadata(self, iptc):
        """
        Tries to find source name in provided IPTC metadata given by 'iptc'.
        Returns empty string if nothing is found.
        :param iptc:
        :return source_name:
        """
        logger.debug('get_image_source_name_by_metadata()')

        source_name = ''

        if (2, 115) in iptc:
            # we have a source
            source_name = iptc[(2, 115)].decode('UTF-8')
        else:
            source_name = ''

        return source_name

    def get_image_author_by_metadata(self, iptc):
        """
        Tries to find author name in provided IPTC metadata given by 'iptc'.
        Returns empty string if nothing is found.
        :param iptc:
        :return author_name:
        """
        logger.debug('get_image_author_by_metadata()')

        author_name = ''

        if (2, 80) in iptc:
            # we have an author
            author_name = iptc[(2, 80)].decode('UTF-8')
        elif (2, 85) in iptc:
            # we have an author title
            author_name = iptc[(2, 85)].decode('UTF-8')
        else:
            author_name = ''

        return author_name

    def get_image_location_by_metadata(self, iptc):
        """
        Tries to find location name in provided IPTC metadata given by 'iptc'.
        Returns empty string if nothing is found.
        :param iptc:
        :return location_str:
        """
        logger.debug('get_image_author_by_metadata()')

        location_str = ''
        locations = []

        if (2, 92) in iptc:
            # we have a Sublocation
            locations.append(iptc[(2, 92)].decode('UTF-8'))
        if (2, 90) in iptc:
            # we have a city
            locations.append(iptc[(2, 90)].decode('UTF-8'))
        if (2, 95) in iptc:
            # we have a Province-State
            locations.append(iptc[(2, 95)].decode('UTF-8'))
        if (2, 101) in iptc:
            # we have a Country
            locations.append(iptc[(2, 101)].decode('UTF-8'))
        location_str = ', '.join(locations)

        return location_str

    def get_image_keywords_by_metadata(self, iptc):
        """
        Tries to find keywords in provided IPTC metadata given by 'iptc'.
        Returns empty string if nothing is found.
        :param iptc:
        :return keywords:
        """
        logger.debug('get_image_source_name_by_metadata()')

        keywords = ''

        if (2, 25) in iptc:
            # we have keywords
            keywords = iptc[(2, 25)].decode('UTF-8')
        else:
            keywords = ''

        return keywords

class WarietyManualFetcher(Observer):
    """docstring for WarietyManualFetcher"""

    def __init__(self, config={}):
        logger.debug('Starting manual fetcher')
        logger.debug('__init__()')
        self.config = config
        self.keep_running = self.config['manual_download']
        self.fetch_dir = self.config['manual_download_folder']
        self.database = wariety_database.WarietyDatabase(self.config)
        Observer.__init__(self)
        if self.keep_running is True:
            self.event_handler = WarietyManualFetchHandler(self.config)
            self.initial_folder_scan(self.fetch_dir)
            self.schedule(self.event_handler, path=self.fetch_dir, recursive=False)
            self.start()

    def __del__(self):
        logger.debug('Stopping manual fetcher')
        logger.debug('__del__()')

    def initial_folder_scan(self, fetch_dir):
        """
        Loops thru all files of the folder given by 'fetch_dir' and checks whether
        each file exists as image in the DB. Images who do not exists in the DB will
        be added.
        :param fetch_dir:
        :return:
        """
        logging.debug('initial_folder_scan()')

        all_image_file_paths = wariety_database.get_all_image_paths_from_folder_by_path(fetch_dir)
        for image_file_path in all_image_file_paths:
            image_id = self.database.exists_image_by_url_or_path(image_file_path)
            if not image_id:
                logging.debug('initial_folder_scan() - add new image')
                my_new_wallpaper = wariety_database.get_empty_image()
                self.event_handler.fill_image_metadata(image_file_path, my_new_wallpaper)
                self.database.add_image_to_database(my_new_wallpaper)
