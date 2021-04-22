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
from pubsub import pub

import wariety_database
import wariety_queue

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


def push_show_icon_animation(self):
    """
    Sends 'show icon animation' message
    :return:
    """
    logger.debug('push_show_icon_animation()')
    pub.sendMessage("show icon animation", event='')


def push_show_balloon_msg(self, title, desc):
    """
    Sends 'show balloon msg' message
    :return:
    """
    logger.debug('show_balloon_msg()')
    pub.sendMessage("show balloon msg", event='', title=title, msg=desc)


class WarietyUpdaterThread(threading.Thread):
    """docstring for WarietyUpdaterThread"""

    def __init__(self, update_schedule=0, config={}):
        """Init Worker Thread Class."""
        logger.debug('Starting updater thread')
        logger.debug('__init__()')

        self.config = config
        self.database = wariety_database.WarietyDatabase(self.config)
        self.current_wallpaper = self.database.get_current_image()

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
        self.backward = False
        self.do_updates = False  # config['change wallpaper']
        self.do_once = False  # On Next
        if int(update_schedule) == 0:
            self.do_updates = False
        else:
            self.do_updates = True
        self.start()

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping updater thread')
        pass

    def set_keep_running(self, new_keep_running):
        logger.debug('set_keep_running({})'.format(str(new_keep_running)))
        self.keep_running = new_keep_running

    def set_seconds_until_fire(self, new_set_seconds_until_fire):
        logger.debug('set_seconds_until_fire({})'.format(new_set_seconds_until_fire))
        self.do_once = True
        self.seconds_until_fire = new_set_seconds_until_fire

    def go_backward(self):
        self.backward = True

    def go_forward(self):
        self.backward = False

    def ensure_filled_queue(self):
        """
        Ensures that the queue is alwayas filled with queue items
        with the status 'QUEUED'
        """
        #logger.debug('ensure_filled_queue()')

        # Set queue status to 'QUEUED'
        _status = wariety_queue.WarietyQueue.queue_statuses['QUEUED']
        wariety_queue.WarietyQueue.instance().queue_status = _status  # Set queue instance status to "QUEUED"!
        _no_of_imgs_in_queue = self.database.get_total_number_of_images('queue', _status)
        # Put new items to the queue in case there are less than 2 items
        if _no_of_imgs_in_queue < 2:
            self.database.push_empty_queue()

    def run(self):
        """Run Worker Thread."""
        logger.debug('run()')
        while self.keep_running:

            self.seconds_until_fire = self.seconds_until_fire - self.check_interval
            if (self.seconds_until_fire <= 0 and self.do_updates) or self.do_once:
                self.do_once = False  # Default is False
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

                _current_image = self.database.get_current_image()
                if self.backward:
                    # Go backward
                    self.backward = False  # Reset

                    # Current
                    self.current_wallpaper = self.database.get_current_image()
                    if self.current_wallpaper.found_at_counter == -1:

                        # Init queue
                        _random_images = self.database.get_random_image()
                        self.current_wallpaper = _random_images[0]
                        update_wallpaper(self.current_wallpaper.image_path)
                        _current_image = self.current_wallpaper
                        self.database.add_currently_seen_by_queue_id(self.current_wallpaper.id)

                        # Update database
                        self.database.set_total_seen_number_by_id(self.current_wallpaper.id)
                        continue

                    # Previous
                    _status = wariety_queue.WarietyQueue.queue_statuses['CURRENT']
                    _current_queue_id = self.database.get_queue_id_by_id_and_status(self.current_wallpaper.id, _status)

                    # Next
                    _previous_queue_ids = self.database.get_previous_queue_ids_by_queue_id(_current_queue_id, 2)
                    if len(_previous_queue_ids) == 0:

                        # We're at the beginning of the queue
                        self.database.set_previously_seen(True)
                        _random_images = self.database.get_random_image()
                        self.current_wallpaper = _random_images[0]
                        update_wallpaper(self.current_wallpaper.image_path)
                        _current_image = self.current_wallpaper

                        # Update database
                        self.database.add_currently_seen_by_queue_id(self.current_wallpaper.id)
                        self.database.set_total_seen_number_by_id(self.current_wallpaper.id)

                    elif len(_previous_queue_ids) == 1:
                        pass
                    elif len(_previous_queue_ids) >= 2:

                        # We're in the middle of the queue
                        self.database.set_previously_seen(True)
                        _next_image = self.database.get_image_by_id(_previous_queue_ids[0]['image_id'])
                        update_wallpaper(_next_image.image_path)
                        _current_image = _next_image

                        # Update database
                        self.database.set_currently_seen_by_queue_id(_previous_queue_ids[0]['id'], _previous_queue_ids[1]['id'])
                        self.database.set_total_seen_number_by_id(_next_image.id)

                elif not self.backward:
                    # Go forward
                    self.backward = False  # Reset

                    # Current
                    self.current_wallpaper = self.database.get_current_image()
                    if self.current_wallpaper.found_at_counter == -1:

                        # Init queue
                        self.current_wallpaper = self.database.get_highest_ranked_image_from_queue()
                        _current_queue_id = self.database.get_queue_id_by_id_and_status(self.current_wallpaper.id)
                        update_wallpaper(self.current_wallpaper.image_path)
                        _current_image = self.current_wallpaper
                        self.database.set_currently_seen_by_queue_id(_current_queue_id)

                        # Update database
                        self.database.set_last_seen_date_by_queue_id(_current_queue_id)
                        self.database.set_total_seen_number_by_id(self.current_wallpaper.id)
                        continue

                    # Previous
                    _status = wariety_queue.WarietyQueue.queue_statuses['CURRENT']
                    _current_queue_id = self.database.get_queue_id_by_id_and_status(self.current_wallpaper.id, _status)
                    self.database.set_previous_seen_by_queue_id(_current_queue_id, -1)

                    # Next
                    _next_images = self.database.get_next_images_from_queue()
                    _next_queue_id = self.database.get_queue_id_by_id_and_status(_next_images[0].id)
                    update_wallpaper(_next_images[0].image_path)
                    _current_image = _next_images[0]
                    self.database.set_currently_seen_by_queue_id(_next_queue_id, _current_queue_id)

                    # Update database
                    self.database.set_last_seen_date_by_queue_id(_next_queue_id)
                    self.database.set_total_seen_number_by_id(_next_images[0].id)

                # Show animation, if necessary
                if self.config['animate_system_tray_icon']:
                    push_show_icon_animation(self)

                # Show balloon message, if necessary
                if self.config['show_balloon_message']:
                    my_title = _current_image.image_name
                    my_desc = self.database.get_image_description_by_id(_current_image.id)
                    push_show_balloon_msg(self, my_title, my_desc)

            else:
                self.ensure_filled_queue()
                time.sleep(self.check_interval)

    def stop(self):
        logger.debug('stop()')
        self.seconds_until_fire = 1
        self.keep_running = False
