#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ctypes
import logging
import threading
import time

import win32con

logger = logging.getLogger(__name__)


def update_wallpaper(new_wallpaper_path):
    """Sets asset given by 'path' as current Desktop wallpaper"""
    logger.debug('update_wallpaper()')

    cs = ctypes.create_string_buffer(new_wallpaper_path.encode('utf-8'))
    ok = ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER, 0, cs, 0)


class WarietyUpdaterThread(threading.Thread):
    """docstring for WarietyUpdaterThread"""

    def __init__(self, update_schedule=0, config={}):
        """Init Worker Thread Class."""
        logger.debug('Starting updater thread')
        logger.debug('__init__()')
        threading.Thread.__init__(self)
        self.updt_sched = int(update_schedule)
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
                self.seconds_until_fire = 60 * self.updt_sched
                update_wallpaper("")  # TODO Check path!
            else:
                time.sleep(self.check_interval)

    def stop(self):
        logger.debug('stop()')
        self.seconds_until_fire = 1
        self.keep_running = False
