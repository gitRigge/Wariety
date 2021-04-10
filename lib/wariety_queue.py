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
import random

from pubsub import pub

import wariety_database

logger = logging.getLogger(__name__)

def to_queue_item(list_of_values, queue_item):
    """
    Expects a list of values and converts them into a
    queue item given by 'queue_item'. Returns the filled
    queue_item.
    Note: the sort order is important!
    Caution: this method sets queue status indirectly!
    :param list_of_values:
    :param queue_item:
    :return: queue_item
    """
    logger.debug('to_queue_item()')
    i = 0
    queue_item.id = list_of_values[i]
    i += 1
    queue_item.image_id = list_of_values[i]
    i += 1
    queue_item.queue_rank = list_of_values[i]
    i += 1
    queue_item.queue_status = list_of_values[i]
    i += 1
    queue_item.queue_seen_date = list_of_values[i]
    i += 1
    queue_item.previous_queue_id = list_of_values[i]
    return queue_item

class WarietyQueue(object):
    """docstring for WarietyQueue"""

    _instance = None

    weight_unseen = 2
    weight_rating = 3
    weight_total_seen = 1
    weight_last_seen = 1
    weight_random = 3

    queue_statuses = {
        'QUEUED': 'QUEUED',
        'DONE': 'DONE',
        'CURRENT': 'CURRENT'
    }

    def __init__(self, config={}):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, config={}):
        if cls._instance is None:
            # Singleton
            cls._instance = cls.__new__(cls)
            logger.debug('Starting queue')
            logger.debug('__init__()')

            # Configuration
            cls.config = config

            # Queue Item properties
            cls.id = ''
            cls.image_id = ''
            cls.queue_rank = 0
            cls.queue_status = cls.queue_statuses['QUEUED']
            cls.queue_seen_date = ''
            cls.previous_queue_id = ''

            # Queue Rankings
            cls.queue_images = []
            cls.queue_rankings = {}

            # DB
            cls.database = wariety_database.WarietyDatabase()

            # Messaging
            pub.subscribe(cls.update_queuer, "empty queue")

        return cls._instance

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping queue')

    def to_dict(self):
        logger.debug('to_dict()')
        queue_item_dict = {
            'id': ['integer primary key', self.id],
            'image_id': ['integer', self.image_id],
            'queue_rank': ['integer', self.queue_rank],
            'queue_status': ['text', self.queue_status],
            'queue_seen_date': ['text', self.queue_seen_date],
            'previous_queue_id': ['integer', self.previous_queue_id]
        }
        return queue_item_dict

    def update_queuer(cls, msg):
        """
        Starts the process of receiving wallpaper images from the database, calculating their rankings and
        sending them to the queue.
        Is called by push message 'empty queue'
        :param msg:
        :return:
        """
        logging.debug('update_downloader(msg)')
        cls.get_queue_images()
        cls.calculate_queue_image_rankings()
        cls.send_queue_images_to_database()
        cls.queue_images.clear()

    def get_queue_images(self):
        """
        Receives a number of wallpapers from the database and fills it in 'queue_images'. The received
        number of images depends on the weights.
        :return:
        """
        logger.debug('get_queue_images()')

        _seen = 0
        self.queue_images = self.queue_images + self.database.get_seen_image(self.weight_unseen, _seen)
        _rating = 5
        self.queue_images = self.queue_images + self.database.get_rated_image(self.weight_rating, _rating)
        _total_seen = 3
        self.queue_images = self.queue_images + self.database.get_seen_image(self.weight_total_seen, _total_seen)
        self.queue_images = self.queue_images + self.database.get_most_recent_seen_image(self.weight_last_seen)
        self.queue_images = self.queue_images + self.database.get_random_image(self.weight_random)

    def calculate_queue_image_rankings(self):
        """
        Calculates the ranking for each image in 'queue_images' based on the weights, the total no. of
        wallpaper images in the databases and the wallpaper change interval.
        Image rankings may be negative!
        :return:
        """
        logger.debug('calculate_queue_image_rankings()')

        _tmp = {}
        _total_number_of_Images = int(self.database.get_total_number_of_images())
        _wp_change_interval = int(self.config['wallpaper_change_interval'])
        factor = _wp_change_interval * 60 * 24 / _total_number_of_Images
        for image in self.queue_images:
            _point = 0
            _days_since_last_seen = int(self.database.get_days_since_last_seen_by_id(image.id))
            # calculate points based on number of days since the image has been shown the last time
            if _days_since_last_seen == -1:
                _point = _point + 10 * factor * self.weight_unseen
            else:
                _point = _point + _days_since_last_seen * factor * self.weight_last_seen
            _total_seens = int(image.total_seen_number)
            if _total_seens == 0:
                _point = _point + 10 * factor * self.weight_unseen
            else:
                _point = _point - _total_seens * factor * self.weight_total_seen
            _ranking = int(image.image_rating)
            _point = _point + _ranking * factor * self.weight_rating
            _random = random.randint(0, 10)
            _point = _point + _random * factor * self.weight_random
            _tmp[image.id] = _point

        self.queue_rankings = _tmp

    def send_queue_images_to_database(self):
        """
        Adds each queue ranking to the database.
        Caution: this method sets queue status indirectly!
        :return:
        """
        logger.debug('send_queue_images_to_database()')

        for img_id in self.queue_rankings:
            _image_id = img_id
            _queue_rank = self.queue_rankings[img_id]
            _queue_status = self.queue_status
            _queue_seen_date = ''
            _previous_queue_id = -1
            _queue_values = [0, _image_id, _queue_rank, _queue_status, _queue_seen_date, _previous_queue_id]
            _queue_item = to_queue_item(_queue_values, WarietyQueue.instance())
            self.database.add_item_to_queue(_queue_item)
