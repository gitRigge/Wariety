#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#  Wariety - A wallpaper manager for MS Windows operating system.
#  Copyright (C) 2024 Roland Rickborn <wariety@gmx.net>
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

import calendar
import datetime
import logging
import sys
import urllib.parse
import urllib.request

import bs4
import requests

logger = logging.getLogger(__name__)
if getattr(sys, 'frozen', False):
    import wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader
else:
    import lib.wariety_wallpaper as wariety_wallpaper
    from lib.downloaders.default_downloader import DefaultDownloader


START_URL = 'https://commons.wikimedia.org/wiki/Commons:Bild_des_Tages'
BASE_URL = 'https://commons.wikimedia.org/wiki/'
DOWNLOADER_TYPE = 'wikimedia'
DOWNLOADER_DESCRIPTION = 'Wikimedia Picture Of The Day'
CAPABILITIES = {'single': 'single', 'many': 'many'}


class WikimediaDownloader(DefaultDownloader):

    def __init__(self, config=None):
        logging.debug('__init__(config) - {}'.format(DOWNLOADER_TYPE))
        self.config = config
        self.load_state(DOWNLOADER_TYPE)
        super().__init__(config)

    def __del__(self):
        logging.debug('__del__() - {}'.format(DOWNLOADER_TYPE))
        self.save_state(DOWNLOADER_TYPE)

    def get_downloader_type(self):
        logging.debug('get_downloader_type()')
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        logging.debug('get_downloader_description()')
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        logging.debug('get_capability()')
        return CAPABILITIES['many']

    def get_base_url(self):
        logging.debug('get_base_url()')
        return BASE_URL

    def get_text_of_valid_sibling(self, elem):
        logging.debug('get_text_of_valid_sibling({})'.format(elem))
        elems = elem.next_siblings
        for e in elems:
            try:
                return e.get_text()
            except:
                pass

    def get_no_of_days_of_month_by_url(self, url):
        logging.debug('get_no_of_days_of_month_by_url({})'.format(url))
        month = 0
        year = 0
        number_of_days_of_month = 999
        year_month = url.split('/')[-1]
        try:
            month = int(year_month.split('-')[-1])
            year = int(year_month.split('-')[0])
            number_of_days_of_month = calendar.monthrange(year,month)[1]
        except:
            number_of_days_of_month = 999
        return number_of_days_of_month

    def get_next_image(self, last_image_counter=0):
        """Retrieves a picture of the day of Wikimedia and returns it
        as an instance of wariety wallpaper. Depending on the counter
        given by 'last_image_counter' returns the next picture.
        """

        logging.debug('get_next_image({})'.format(last_image_counter))

        # Generate empty image
        next_image = wariety_wallpaper.WarietyWallpaper()

        # Get content
        session = requests.Session()
        session.proxies.update(self.proxies)
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/131.0.2903.86",
            'accept': '"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"',
            'referer': 'https://dont_worry.org',
        }
        response = session.get(START_URL, stream=True, verify=False, headers=headers)
        content = response.content

        # Receive image data
        soup = bs4.BeautifulSoup(content, 'html.parser')
        plainlist = soup.find('div', {'class': 'plainlist'})
        hlist = plainlist.findAll('li', {'class': 'hlist'})

        months_list = []

        # Get all month pages
        for hlist_item in hlist:
            hlist_li_href = hlist_item.findAll('a', href=True)
            for hlist_li_href_item in hlist_li_href:
                month_page_url = urllib.parse.urljoin(BASE_URL, hlist_li_href_item['href'])
                months_list.append(month_page_url)

        # Grab URL to images
        counter = -1
        days_counter = 0

        # for month_page in months_list:
        while months_list:
            month_page = months_list.pop(0)

            # Speed up things by counting days per month
            days_counter = days_counter + self.get_no_of_days_of_month_by_url(month_page)
            if days_counter < last_image_counter:
                continue
            else:
                page = urllib.request.urlopen(month_page).read()
                soup = bs4.BeautifulSoup(page, 'html.parser')
                potd_tables = soup.findAll('table')
                for potd_table in potd_tables:
                    hyperlinks = potd_table.findAll('a', {'class': 'image'})
                    for hyperlink in hyperlinks:
                        counter = counter + 1
                        if counter == last_image_counter:

                            # Return one image after the last transfered
                            next_image.image_url = urllib.parse.urljoin(BASE_URL, hyperlink['href'])
                            if (next_image.image_url.endswith('jpg') or next_image.image_url.endswith('jpeg') or next_image.image_url.endswith('png')):

                                # We just want png or jpeg
                                # Collect image data
                                image_page = urllib.request.urlopen(next_image.image_url).read()
                                image_soup = bs4.BeautifulSoup(image_page, 'html.parser')
                                image_file = image_soup.find(id='file')
                                target_url = image_file.a
                                file_info_section = image_soup.find('table', {'class': 'fileinfotpl-type-information'})

                                # Fill image data
                                try:
                                    file_location_section = file_info_section.find('td', text='Location')
                                    next_image.location = self.get_text_of_valid_sibling(file_location_section).strip().split('\n')[0]
                                except:
                                    next_image.location = ''
                                try:
                                    file_author_section = file_info_section.find('td', text='Author')
                                    next_image.image_author = self.get_text_of_valid_sibling(file_author_section).strip().split('\n')[0]
                                except:
                                    next_image.image_author = ''
                                try:
                                    file_keywords_section = file_info_section.find('td', text='Keywords')
                                    next_image.keywords = self.get_text_of_valid_sibling(file_keywords_section).strip().split('\n')[0]
                                except:
                                    next_image.keywords = ''
                                unquoted_target_url = urllib.parse.unquote(target_url['href'])
                                try:
                                    next_image.image_name = unquoted_target_url.split('/')[-1]
                                except:
                                    next_image.image_name = ''
                                next_image.source_url = urllib.parse.unquote(next_image.image_url)
                                next_image.source_type = DOWNLOADER_TYPE
                                next_image.source_name = DOWNLOADER_DESCRIPTION
                                next_image.image_url = unquoted_target_url
                                next_image.found_at_counter = counter

                                # Store state
                                self.state['last_image_counter'] = next_image.found_at_counter
                                startdate = datetime.datetime.now().strftime('%Y%m%d')
                                self.state['startdate'] = startdate
                                self.state['idx'] = 0

                                return next_image
                            else:
                                counter = counter - 1
                                continue
