#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ctypes
import logging
import sys
import threading
import time

import win32con

import wariety_database

logger = logging.getLogger(__name__)
if getattr(sys, 'frozen', False):
    from wariety.wariety import __status__ as __status__
else:
    try:
        from wariety import __status__ as __status__
    except ImportError:
        logger.debug('get_download_folder_size() - ImportError'.format())
        __status__ = 'Development'


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
        if __status__ == 'Development':
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
                if __status__ == 'Development':
                    logger.debug('__status__ == "Development"')
                    self.seconds_until_fire = 5 * self.updt_sched
                else:
                    self.seconds_until_fire = 60 * self.updt_sched
                my_image = self.database.get_random_image()
                update_wallpaper(my_image.image_path)
            else:
                time.sleep(self.check_interval)

    def stop(self):
        logger.debug('stop()')
        self.seconds_until_fire = 1
        self.keep_running = False
