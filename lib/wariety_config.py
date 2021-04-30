#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Wariety - A wallpaper manager for MS Windows operating system.
#  Copyright (C) 2021 Roland Rickborn <wariety@gmx.net>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see https://www.gnu.org/licenses/.

import configparser
import glob
import importlib
import inspect
import logging
import os
import sys
import winreg

from cryptography.fernet import Fernet
from pubsub import pub

import wariety_key

logger = logging.getLogger(__name__)


class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        return winreg.ExpandEnvironmentStrings(value.replace("'", ""))



class WarietyConfig(object):
    """docstring for WarietyConfig"""
    
    def __init__(self, config_file):
        logger.debug('Starting config')
        logger.debug('__init__({})'.format(config_file))
        self.key = wariety_key.WarietyKey().key

        # General
        self.start_at_startup = False
        self.wallpaper_change = False
        self.wallpaper_change_interval = 8
        self.change_wallpaper_at_startup = False
        self.download_wallpaper = False
        self.download_wallpaper_interval = 8
        self.download_wallpaper_folder = r'%LOCALAPPDATA%\Wariety\Downloaded'
        self.max_wallpaper_folder = False
        self.max_wallpaper_folder_size = 128
        self.manual_download = False
        self.manual_download_folder = r'%LOCALAPPDATA%\Wariety\Fetched'
        self.animate_system_tray_icon = False
        self.show_balloon_message = False
        self.plugin_folder = r'%LOCALAPPDATA%\Wariety\Plugins'

        # Proxy
        self.proxy_enable = False
        self.proxy_address = ''
        self.proxy_port = 8080
        self.proxy_username = ''
        self.proxy_pw_encrypted = ''
        self.proxies = {}

        # Built-in Sources
        self.builtin_downloaders = {}
        self.available_builtin_downloaders = {}

        # External Sources
        self.external_downloaders = {}
        self.available_external_downloaders = {}

        self.config = configparser.ConfigParser(interpolation=EnvInterpolation())
        self.config_file = config_file

        # Get configuration
        self.read_config_file()
        self.read_config()

        # Fill proxies dict
        self.setup_proxies()

        # Init Plugins Folder
        self.init_folders()

        # Find built-in downloaders
        if getattr(sys, 'frozen', False):
            downloaders_dir = sys._MEIPASS + '/lib/downloaders'
        else:
            downloaders_dir = 'lib/downloaders'
        downloaders_path = os.path.abspath(downloaders_dir)
        self.identify_available_downloaders(downloaders_path, self.available_builtin_downloaders)
        self.assign_configured_with_available_downloaders(self.available_builtin_downloaders,
                                                          self.builtin_downloaders, 'Sources')

        # Find external downloaders
        downloaders_path = os.path.abspath(self.plugin_folder)
        self.identify_available_downloaders(downloaders_path, self.available_external_downloaders)
        self.assign_configured_with_available_downloaders(self.available_external_downloaders,
                                                          self.external_downloaders, 'External Sources')

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping config')

    def setup_proxies(self):
        logger.debug('setup_proxies()')
        if self.proxy_enable:
            if self.proxy_username != '':
                self.proxies['http'] = '{}:{}@{}:{}'.format(self.proxy_username,
                                                            self.proxy_pw_encrypted,
                                                            self.proxy_address,
                                                            self.proxy_port)
                self.proxies['https'] = '{}:{}@{}:{}'.format(self.proxy_username,
                                                            self.proxy_pw_encrypted,
                                                            self.proxy_address,
                                                            self.proxy_port)
            else:
                self.proxies['http'] = '{}:{}'.format(self.proxy_address, self.proxy_port)
                self.proxies['https'] = '{}:{}'.format(self.proxy_address, self.proxy_port)
            os.environ['HTTP_PROXY'] = self.proxies['http']
            os.environ['HTTPS_PROXY'] = self.proxies['https']

    def init_folders(self):
        """
        Checks for required folders 'self.download_wallpaper_folder', 'self.manual_download_folder'
        and 'self.plugin_folder' and creates it if they do not yet exist.
        :return:
        """
        logger.debug('init_folders()')
        dir_path = os.path.abspath(self.download_wallpaper_folder)
        os.makedirs(dir_path, exist_ok=True)
        dir_path = os.path.abspath(self.manual_download_folder)
        os.makedirs(dir_path, exist_ok=True)
        dir_path = os.path.abspath(self.plugin_folder)
        os.makedirs(dir_path, exist_ok=True)

    def on_close(self):
        """
        Update, write config to file and then push.
        :return:
        """
        logger.debug('on_close()')
        self.set_config()
        self.write_config_file()
        self.push_updated_config()

    def read_config_file(self):
        """
        Tries to read config from file. If config file does not exist, creates config file,
        adds sectors 'General', 'Sources' and 'External Sources' and fills with default values.
        :return:
        """
        logger.debug('read_config_file()')
        if os.path.isfile(self.config_file):
            self.config.read(self.config_file)
        else:
            logger.debug('read_config_file() - No config file found.')
            self.config.add_section('General')
            self.config.add_section('Proxy')
            self.config.add_section('Sources')
            self.config.add_section('External Sources')
            self.config.read(self.config_file)
            self.set_config()
            self.write_config_file()

    def write_config_file(self):
        """
        Writes current config to file.
        :return:
        """
        logger.debug('write_config_file()')
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    def read_config(self):
        """
        Parses config and assigns it to instance variables.
        Sets default values in case of fallback.
        :return:
        """
        logger.debug('read_config()')
        # General
        self.start_at_startup = self.config['General'].getboolean('start_at_startup',
                                                                  fallback=self.start_at_startup)
        self.wallpaper_change = self.config['General'].getboolean('wallpaper_change',
                                                                  fallback=self.wallpaper_change)
        self.wallpaper_change_interval = self.config['General'].getint('wallpaper_change_interval',
                                                                       fallback=self.wallpaper_change_interval)
        self.change_wallpaper_at_startup = self.config['General'].getboolean('change_wallpaper_at_startup',
                                                                             fallback=self.change_wallpaper_at_startup)
        self.download_wallpaper = self.config['General'].getboolean('download_wallpaper',
                                                                    fallback=self.download_wallpaper)
        self.download_wallpaper_interval = self.config['General'].getint('download_wallpaper_interval',
                                                                         fallback=self.download_wallpaper_interval)
        self.download_wallpaper_folder = self.config['General'].get('download_wallpaper_folder',
                                                                    fallback=os.path.expandvars(r'%LOCALAPPDATA%\Wariety\Downloaded'))
        self.max_wallpaper_folder = self.config['General'].getboolean('max_wallpaper_folder',
                                                                      fallback=self.max_wallpaper_folder)
        self.max_wallpaper_folder_size = self.config['General'].getint('max_wallpaper_folder_size',
                                                                       fallback=self.max_wallpaper_folder_size)
        self.manual_download = self.config['General'].getboolean('manual_download',
                                                                 fallback=self.manual_download)
        self.manual_download_folder = self.config['General'].get('manual_download_folder',
                                                                 fallback=os.path.expandvars(r'%LOCALAPPDATA%\Wariety\Fetched'))
        self.animate_system_tray_icon = self.config['General'].getboolean('animate_system_tray_icon',
                                                                          fallback=self.animate_system_tray_icon)
        self.show_balloon_message = self.config['General'].getboolean('show_balloon_message',
                                                                      fallback=self.show_balloon_message)
        self.plugin_folder = self.config['General'].get('plugin_folder',
                                                        fallback=os.path.expandvars(r'%LOCALAPPDATA%\Wariety\Plugins'))

        # Proxy
        self.proxy_enable = self.config['Proxy'].getboolean('enable', fallback=self.proxy_enable)
        self.proxy_address = self.config['Proxy'].get('address', fallback=self.proxy_address)
        self.proxy_port = self.config['Proxy'].getint('port', fallback=self.proxy_port)
        self.proxy_username = self.config['Proxy'].get('username', fallback=self.proxy_username)
        _pw = self.config['Proxy'].get('password', fallback='')
        self.proxy_pw_encrypted = self.decrypt_pw(_pw)

        # Sources
        for bltin_src in self.config['Sources']:
            self.builtin_downloaders[bltin_src] = self.config['Sources'].getboolean(bltin_src)

        # External Sources
        for ext_src in self.config['External Sources']:
            self.external_downloaders[ext_src] = self.config['External Sources'].getboolean(ext_src)

    def set_config(self):
        """
        Sets config taken from instance variables.
        :return:
        """
        logger.debug('set_config()')
        # General
        self.config.set('General', 'start_at_startup', str(self.start_at_startup))
        self.config.set('General', 'wallpaper_change', str(self.wallpaper_change))
        self.config.set('General', 'wallpaper_change_interval', str(self.wallpaper_change_interval))
        self.config.set('General', 'change_wallpaper_at_startup', str(self.change_wallpaper_at_startup))
        self.config.set('General', 'download_wallpaper', str(self.download_wallpaper))
        self.config.set('General', 'download_wallpaper_interval', str(self.download_wallpaper_interval))
        self.config.set('General', 'download_wallpaper_folder', str(os.path.expandvars(self.download_wallpaper_folder)))
        self.config.set('General', 'max_wallpaper_folder', str(self.max_wallpaper_folder))
        self.config.set('General', 'max_wallpaper_folder_size', str(self.max_wallpaper_folder_size))
        self.config.set('General', 'manual_download', str(self.manual_download))
        self.config.set('General', 'manual_download_folder', str(os.path.expandvars(self.manual_download_folder)))
        self.config.set('General', 'animate_system_tray_icon', str(self.animate_system_tray_icon))
        self.config.set('General', 'show_balloon_message', str(self.show_balloon_message))
        self.config.set('General', 'plugin_folder', str(os.path.expandvars(self.plugin_folder)))

        # Proxy
        self.config.set('Proxy', 'enable', str(self.proxy_enable))
        self.config.set('Proxy', 'address', str(self.proxy_address))
        self.config.set('Proxy', 'port', str(self.proxy_port))
        self.config.set('Proxy', 'username', str(self.proxy_username))
        _pw = self.encrypt_pw(self.proxy_pw_encrypted)
        self.config.set('Proxy', 'password', _pw)

        # Built-in Downloaders
        for bltin_src in self.builtin_downloaders:
            self.config.set('Sources', bltin_src, str(self.builtin_downloaders[bltin_src]))

        # External Downloaders
        for ext_src in self.external_downloaders:
            self.config.set('External Sources', ext_src, str(self.external_downloaders[ext_src]))

    def push_updated_config(self):
        """
        Sends 'config updated' message
        :return:
        """
        logger.debug('push_updated_config()')
        pub.sendMessage("config updated", msg=self.to_dict())

    def to_dict(self):
        """
        Takes instance variables and puts it into a dict. Returns the dict.
        :return my_config:
        """
        logger.debug('to_dict()')
        my_config = {
            'start_at_startup': self.start_at_startup,
            'wallpaper_change': self.wallpaper_change,
            'wallpaper_change_interval': self.wallpaper_change_interval,
            'change_wallpaper_at_startup': self.change_wallpaper_at_startup,
            'download_wallpaper': self.download_wallpaper,
            'download_wallpaper_interval': self.download_wallpaper_interval,
            'download_wallpaper_folder': self.download_wallpaper_folder,
            'max_wallpaper_folder': self.max_wallpaper_folder,
            'max_wallpaper_folder_size': self.max_wallpaper_folder_size,
            'manual_download': self.manual_download,
            'manual_download_folder': self.manual_download_folder,
            'animate_system_tray_icon': self.animate_system_tray_icon,
            'show_balloon_message': self.show_balloon_message,
            'plugin_folder': self.plugin_folder,
            'enable': self.proxy_enable,
            'address': self.proxy_address,
            'port': self.proxy_port,
            'username': self.proxy_username,
            'password': self.proxy_pw_encrypted,
        }
        for bltin_src in self.builtin_downloaders:
            my_config[bltin_src] = self.builtin_downloaders[bltin_src]

        for ext_src in self.external_downloaders:
            my_config[ext_src] = self.external_downloaders[ext_src]

        return my_config

    def identify_available_downloaders(self, downloaders_path, downloaders_list):
        """
        Searches for py files in 'downloaders_path', identifies modules which inherit
        a class 'DefaultDownloader' and a methode 'get_downloader_type' and imports those
        which have a type. Adds all found downloaders to the array 'downloaders_list'
        :return:
        """
        logger.debug('identify_available_downloaders({}, downloaders_list)'.format(downloaders_path))
        candidates = glob.glob(os.path.join(downloaders_path, '*.py'))
        for candidate in candidates:
            my_module_name = inspect.getmodulename(candidate)
            try:
                sys.path.insert(1, downloaders_path)  # TODO Check if necessary!
                my_module = importlib.import_module(my_module_name)
                # Check whether it inherits from 'DefaultDownloader'
                inherits_from_DefaultDownloader = False
                for i in range(0, len(inspect.getmembers(my_module, inspect.isclass))):
                    if inspect.getmembers(my_module, inspect.isclass)[i][0] == 'DefaultDownloader' and len(inspect.getmembers(my_module, inspect.isclass)) >= 2:
                        inherits_from_DefaultDownloader = True

                if inherits_from_DefaultDownloader:
                    if inspect.getmembers(my_module, inspect.isclass)[0][0] == 'DefaultDownloader':
                        my_class_name = inspect.getmembers(my_module, inspect.isclass)[1][0]
                    else:
                        my_class_name = inspect.getmembers(my_module, inspect.isclass)[0][0]
                    my_class = getattr(my_module, my_class_name)
                    my_instance = my_class(self.config)
                    _type = my_instance.get_downloader_type()
                    if _type != '':
                        logger.debug('identify_available_downloaders() - found type "{}"'.format(_type))
                        description = my_instance.get_downloader_description()
                        capability = my_instance.get_capability()
                        base_url = my_instance.get_base_url()
                        downloaders_list[_type] = (description,
                                                   capability,
                                                   base_url,
                                                   my_module_name,
                                                   my_module,
                                                   my_instance)
                    else:
                        logger.debug('identify_available_downloaders() - {}'.format('Is DefaultDownloader, no import'))
                else:
                    logger.debug('identify_available_downloaders() - {}'.format('Is no Downloader, no import'))
            except:
                e = sys.exc_info()[0]
                logger.debug('identify_available_downloaders() - Error: {}'.format(e))

    def assign_configured_with_available_downloaders(self, available_downloaders, configured_downloaders, section):
        """
        Compares the available downloaders 'available_downloaders' with the downloaders known to the
        config 'configured_downloaders' (independent whether the configured downloads are enabled or disabled).
        Adds unknown downloaders with pre-set state FALSE to the config.
        Removes unavailable downloaders from the config.
        :return:
        """
        logger.debug('assign_configured_with_available_downloaders(avbl_dldrs, cfgr_dldrs, {})'.format(section))
        for dl in available_downloaders:
            if dl not in configured_downloaders:
                logger.debug('assign_configured_with_available_downloaders() - New downloader {} added'.format(dl))
                configured_downloaders[dl] = False
            else:
                pass

        _need_to_delete = []
        for dl in configured_downloaders:
            if dl not in available_downloaders:
                logger.debug('assign_configured_with_available_downloaders() - Unavailable downloader {} deleted'.format(dl))
                _need_to_delete.append(dl)
            else:
                pass

        for dl in _need_to_delete:
            del configured_downloaders[dl]
            self.config.remove_option(section, dl)

    def decrypt_pw(self, pw):
        """
        Returns the decrypted password given by 'pw' using the
        static key 'k'. Returns empty string in case of error.
        :param pw:
        :return retVal:
        """
        retVal = ''

        logger.debug('decrypt_pw(***)')
        f = Fernet(self.key)
        try:
            retVal = f.decrypt(bytes(pw, 'utf-8'))
        except:
            retVal = b''
        return retVal.decode('UTF-8')

    def encrypt_pw(self, pw):
        """
        Returns the encrypted password given by 'pw' using the
        static key 'k'.
        :param pw:
        :return retVal:
        """
        retVal = ''

        logger.debug('encrypt_pw(***)')
        f = Fernet(self.key)
        retVal = f.encrypt(bytes(pw, 'utf-8'))
        return retVal.decode('UTF-8')