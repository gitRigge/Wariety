#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Wariety - A wallpaper manager for MS Windows operating system.
# Copyright (C) 2024  Roland Rickborn <wariety@gmx.net>
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
import re
import sys
import threading

import requests
from pubsub import pub

logger = logging.getLogger(__name__)


def get_remote_version():
    """
    :return:
    """

    logger.debug('get_remote_version()')

    # Static URL to Wariety main at Github
    url = 'https://github.com/gitRigge/Wariety/blob/master/wariety/wariety.py'

    ret_val = '0.0.0'

    version_search = '(__version__).*([0-9]\.[0-9]\.[0-9])'
    status_search1 = '(__status__).*'
    status_search2 = '&quot;([^&]*)&quot;'
    response = requests.get(url)

    result1 = re.search(version_search, response.text)
    result2 = re.search(status_search1, response.text)

    if result1:
        ret_val = result1.group(2)
    else:
        ret_val = '0.0.0'

    _status = ''
    if result2:
        result3 = re.search(status_search2, result2.group(0))
        if result3:
            _status = result3.group(1)
        else:
            _status = 'Test'  # TODO Replace with "ENUM"
    else:
        _status = 'Test'  # TODO Replace with "ENUM"

    if _status != 'Release':  # TODO Replace with "ENUM"
        ret_val = '0.0.0'

    return ret_val


def is_update_available(local_version_str, remote_version_str):
    """
    Compares the local version given by 'local_version_str' with
    the remote version given by 'remote_version_str'. Returns True
    if the remote version is higher than the local version. Otherwise,
    returns False.
    :param local_version_str:
    :param remote_version_str:
    :return ret_val:
    """

    logger.debug('is_update_available({}, {})'.format(local_version_str, remote_version_str))

    ret_val = False

    local_version = 0
    try:
        local_version = int(local_version_str.replace('.', ''))
        logger.debug('is_update_available() - local version = {}'.format(local_version))
    except:
        local_version = 0

    remote_version = 0
    try:
        remote_version = int(remote_version_str.replace('.', ''))
        logger.debug('is_update_available() - remote version = {}'.format(remote_version))
    except:
        remote_version = 0

    if remote_version > local_version:
        ret_val = True
    else:
        ret_val = False

    return ret_val


def push_app_update(self):
    """
    Sends 'show app update' message
    :return:
    """
    logger.debug('push_app_update()')
    pub.sendMessage("show app update", event='')


def push_version_str(self, msg, update_available):
    """
    Sends 'show version str' message
    :return:
    """
    logger.debug('push_version_str()')
    pub.sendMessage("show version str", event='', msg=msg, update_available=update_available)


class WarietyAppUpdaterThread(threading.Thread):
    """docstring for WarietyAppUpdaterThread"""

    def __init__(self, show_balloon=False, show_version_str=False):
        """Init Worker Thread Class."""
        logger.debug('Starting app updater thread')
        logger.debug('__init__()')
        self.my_version = ''
        self.show_balloon = show_balloon
        self.show_version_str = show_version_str

        threading.Thread.__init__(self)

        if getattr(sys, 'frozen', False):
            import wariety.wariety
            self.my_version = wariety.wariety.__version__
        else:
            from wariety import __version__
            self.my_version = __version__

        self.start()

    def run(self):
        """Run Worker Thread."""
        logger.debug('run()')

        remote_version = get_remote_version()
        is_updateable = is_update_available(self.my_version, remote_version)
        if is_updateable:
            if self.show_balloon:
                push_app_update(self)
            if self.show_version_str:
                push_version_str(self, remote_version, is_updateable)
        else:
            remote_version = self.my_version
            if self.show_version_str:
                push_version_str(self, remote_version, is_updateable)
