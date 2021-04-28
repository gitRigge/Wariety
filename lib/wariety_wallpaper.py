#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Wariety - A wallpaper manager for MS Windows operating system.
# Copyright (C) 2021  Roland Rickborn <wariety@gmx.net>
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

logger = logging.getLogger(__name__)


def to_wallpaper(list_of_values, wallpaper):
    """
    Receives both, a dictionary with wallpaper properties and a wallpaper
    object. Writes then all properties of the dictionary to the wallpaper
    object and returns it.
    :param list_of_values:
    :param wallpaper:
    :return wallpaper:
    """
    logger.debug('to_wallpaper()')
    i = 0
    wallpaper.id = list_of_values[i]
    i += 1
    wallpaper.image_name = list_of_values[i]
    i += 1
    wallpaper.image_md5_hash = list_of_values[i]
    i += 1
    wallpaper.image_path = list_of_values[i]
    i += 1
    wallpaper.source_url = list_of_values[i]
    i += 1
    wallpaper.source_type = list_of_values[i]
    i += 1
    wallpaper.image_author = list_of_values[i]
    i += 1
    wallpaper.source_name = list_of_values[i]
    i += 1
    wallpaper.image_rating = list_of_values[i]
    i += 1
    wallpaper.image_url = list_of_values[i]
    i += 1
    wallpaper.location = list_of_values[i]
    i += 1
    wallpaper.keywords = list_of_values[i]
    i += 1
    wallpaper.source_location = list_of_values[i]
    i += 1
    wallpaper.found_at_counter = list_of_values[i]
    i += 1
    wallpaper.image_orientation = list_of_values[i]
    i += 1
    wallpaper.download_date = list_of_values[i]
    i += 1
    wallpaper.status = list_of_values[i]
    i += 1
    wallpaper.total_seen_number = list_of_values[i]
    i += 1
    wallpaper.image_favorite = list_of_values[i]
    return wallpaper


class WarietyWallpaper(object):
    """docstring for WarietyWallpaper"""

    wallpaper_orientations = {
        'landscape': 'landscape',
        'portrait': 'portrait'
        }

    wallpaper_statuses = {
        'DOWNLOADED': 'DOWNLOADED',
        'DELETED': 'DELETED'
    }

    def __init__(self):
        logger.debug('Starting wallpaper')
        logger.debug('__init__()')

        # Wallpaper Item properties
        self.id = ''
        self.image_name = ''
        self.image_md5_hash = ''
        self.image_path = ''
        self.source_url = ''
        self.source_type = ''
        self.image_author = ''
        self.source_name = ''
        self.image_rating = 0
        self.image_url = ''
        self.location = ''
        self.keywords = ''
        self.source_location = ''
        self.found_at_counter = 0
        self.image_orientation = 'landscape'
        self.download_date = ''
        self.status = ''
        self.total_seen_number = 0
        self.image_favorite = 0

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping wallpaper')

    def to_dict(self):
        """
        Returns all wallpaper properties as one dictionary.
        :return my_image:
        """
        logger.debug('to_dict()')
        my_image = {
            'id': ['integer primary key', self.id],
            'image_name': ['text', self.image_name],
            'image_md5_hash': ['text', self.image_md5_hash],
            'image_path': ['text', self.image_path],
            'source_url': ['text', self.source_url],
            'source_type': ['text', self.source_type],
            'image_author': ['text', self.image_author],
            'source_name': ['text', self.source_name],
            'image_rating': ['integer', self.image_rating],
            'image_url': ['text', self.image_url],
            'location': ['text', self.location],
            'keywords': ['text', self.keywords],
            'source_location': ['text', self.source_location],
            'found_at_counter': ['integer', self.found_at_counter],
            'image_orientation': ['text', self.image_orientation],
            'download_date': ['text', self.download_date],
            'status': ['text', self.status],
            'total_seen_number': ['integer', self.total_seen_number],
            'image_favorite': ['integer', self.image_favorite],
        }
        return my_image
