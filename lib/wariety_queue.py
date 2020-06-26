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

import logging

logger = logging.getLogger(__name__)


def to_queue(list_of_values, queue):
    logger.debug('to_wallpaper()')
    i = 0
    queue.id = list_of_values[i]
    i += 1
    queue.image_id = list_of_values[i]
    return queue

class WarietyQueue(object):
    """docstring for WarietyQueue"""

    _instance = None

    weight_unseen = 0
    weight_rating = 0
    weigth_total_seen = 0
    weight_last_seen = 0
    weight_random = 0

    queue_statuses = {
        'QUEUED': 'QUEUED',
        'DONE': 'DONE'
    }

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            logger.debug('Starting queue')
            logger.debug('__init__()')
            cls.id = ''
            cls.image_id = ''
            cls.rank = 0
            cls.status = 'QUEUED'
        return cls._instance

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping queue')

    def to_dict(self):
        logger.debug('to_dict()')
        my_queue = {
            'id': ['integer primary key', self.id],
            'image_id': ['integer', self.image_id],
            'rank': ['integer', self.rank],
            'status': ['text', self.status]
        }
        return my_queue
