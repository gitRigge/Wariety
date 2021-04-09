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

import ctypes
import logging
import sys
import threading
import time

import win32con

import wariety_database

logger = logging.getLogger(__name__)


def update_wallpaper(new_wallpaper_path):
    """
    Sets asset given by 'path' as current Desktop wallpaper
    :param new_wallpaper_path:
    :return:
    """
    logger.debug('update_wallpaper({})'.format(new_wallpaper_path))

    cs = ctypes.create_string_buffer(new_wallpaper_path.encode('utf-8'))
    ok = ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, cs, 0)


class WarietyUpdaterThread(threading.Thread):
    """docstring for WarietyUpdaterThread"""

    def __init__(self, update_schedule=0, config={}):
        """Init Worker Thread Class."""
        logger.debug('Starting updater thread')
        logger.debug('__init__()')
        self.config = config
        self.database = wariety_database.WarietyDatabase(self.config)
        threading.Thread.__init__(self)

        self.updt_sched = int(update_schedule)
        if getattr(sys, 'frozen', False):
            import wariety.wariety
            my_status = wariety.wariety.__status__
        else:
            from wariety import __status__
            my_status = __status__
        if my_status == 'Development':
            logger.debug('__status__ == "Development"')
            self.seconds_until_fire = 5 * int(update_schedule)
        else:
            self.seconds_until_fire = 60 * int(update_schedule)
        self.check_interval = 1
        self.keep_running = True
        if int(update_schedule) == 0:
            self.do_updates = False
        else:
            self.do_updates = True
        self.start()

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping updater thread')
        pass

    def run(self):
        """Run Worker Thread."""
        logger.debug('run()')
        while self.keep_running:
            self.seconds_until_fire = self.seconds_until_fire - self.check_interval
            if self.seconds_until_fire == 0:
                if getattr(sys, 'frozen', False):
                    import wariety.wariety
                    my_status = wariety.wariety.__status__
                else:
                    from wariety import __status__
                    my_status = __status__
                if my_status == 'Development':
                    logger.debug('__status__ == "Development"')
                    self.seconds_until_fire = 5 * self.updt_sched
                else:
                    self.seconds_until_fire = 60 * self.updt_sched

                my_images = self.database.get_next_images_from_queue(1)

                # Queue management
                if my_images[0].found_at_counter != -1:
                    my_queue_id = self.database.get_queue_id_by_id(my_images[0].id)
                    _no_of_imgs_in_queue = self.database.get_total_number_of_images('queue', 'QUEUED')
                    if _no_of_imgs_in_queue < 2:
                        self.database.push_empty_queue()
                    self.database.set_currently_seeing_by_queue_id(my_queue_id)
                    update_wallpaper(my_images[0].image_path)
                    self.database.set_last_seen_date_by_queue_id(my_queue_id)
                    self.database.set_total_seen_number_by_id(my_images[0].id)
                else:
                    self.database.push_empty_queue()
            else:
                time.sleep(self.check_interval)

    def stop(self):
        logger.debug('stop()')
        self.seconds_until_fire = 1
        self.keep_running = False
