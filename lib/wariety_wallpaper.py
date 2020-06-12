#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

logger = logging.getLogger(__name__)


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
        self.id = ''
        self.image_name = ''
        self.image_md5_hash = ''
        self.image_path = ''
        self.source_url = ''
        self.source_type = ''
        self.image_author = ''
        self.source_name = ''
        self.image_rating = ''
        self.image_url = ''
        self.location = ''
        self.keywords = ''
        self.source_location = ''
        self.found_at_counter = 0
        self.image_orientation = 'landscape'
        self.download_date = ''
        self.status = ''

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping wallpaper')

    def to_dict(self):
        logger.debug('to_dict()')
        my_image = {
            'id':['integer primary key', self.id],
            'image_name':['text', self.image_name],
            'image_md5_hash':['text', self.image_md5_hash],
            'image_path':['text', self.image_path],
            'source_url':['t ext', self.source_url],
            'source_type':['text', self.source_type],
            'image_author':['text', self.image_author],
            'source_name':['text', self.source_name],
            'image_rating':['integer', self.image_rating],
            'image_url':['text', self.image_url],
            'location':['text', self.location],
            'keywords':['text', self.keywords],
            'source_location':['text', self.source_location],
            'found_at_counter':['integer', self.found_at_counter],
            'image_orientation':['text', self.image_orientation],
            'download_date':['text', self.download_date],
            'status':['text', self.status]
        }
        return my_image

    def to_wallpaper(self, list_of_values, wallpaper):
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
        return wallpaper