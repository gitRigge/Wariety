#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import glob
import imghdr
import os
import sys

sys.path.insert(1, '../lib')
import wariety_wallpaper

START_URL = 'http://...'
BASE_URL = 'http://...'
DOWNLOADER_TYPE = 'spotlight'
CAPABILITIES = {'single': 'single', 'many': 'many'}

def get_next_image(last_image_counter=0):
    """Loops through all locally stored Windows Spotlight assets
    and copies and returns the latest asset which has the same orientation as the screen
    """
    next_image = wariety_wallpaper.WarietyWallpaper()
    counter = -1
    localappdata = os.environ['LOCALAPPDATA']
    localstate_assests = r'\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
    list_of_files = sorted(glob.glob(localappdata+localstate_assests+'\*'), key=os.path.getmtime, reverse=True)
    for asset in list_of_files:
        counter = counter + 1
        if counter == last_image_counter:
            extension = imghdr.what(asset)
            if extension in ['jpeg', 'jpg', 'png']:
                # Generate pseudo url
                try:
                    next_image.image_name = os.path.split(asset)[1].split('\\')[-1]
                except:
                    next_image.image_name = ''
                next_image.source_url = 'https://docs.microsoft.com/en-us/windows/configuration/windows-spotlight'
                next_image.source_type = DOWNLOADER_TYPE
                next_image.source_name = 'Microsoft Spotlight'
                next_image.image_url = asset
                next_image.found_at_counter = last_image_counter + 1
                return next_image

def get_downloader_type():
    return DOWNLOADER_TYPE

def get_capability():
    return CAPABILITIES['many']