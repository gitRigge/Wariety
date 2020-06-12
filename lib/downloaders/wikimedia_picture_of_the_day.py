#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import calendar
import logging
import sys
import urllib.parse
import urllib.request

import bs4

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

    def get_downloader_type(self):
        return DOWNLOADER_TYPE

    def get_downloader_description(self):
        return DOWNLOADER_DESCRIPTION

    def get_capability(self):
        return CAPABILITIES['many']

    def get_base_url(self):
        return BASE_URL

    def get_next_image(self, last_image_counter=0):
        """Retrieves a picture of the day of Wikimedia and returns it
        as an instance of wariety wallpaper. Depending on the counter
        given by 'last_image_counter' returns the next picture.
        """
        next_image = wariety_wallpaper.WarietyWallpaper()
        page = urllib.request.urlopen(START_URL).read()
        soup = bs4.BeautifulSoup(page, 'html.parser')
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
        #for month_page in months_list:
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
                                image_page = urllib.request.urlopen(next_image.image_url).read()
                                image_soup = bs4.BeautifulSoup(image_page, 'html.parser')
                                image_file = image_soup.find(id='file')
                                target_url = image_file.a
                                file_info_section = image_soup.find('table', {'class': 'fileinfotpl-type-information'})
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
                                next_image.source_name = 'Wikimedia Bild des Tages'
                                next_image.image_url = unquoted_target_url
                                next_image.found_at_counter = counter
                                return next_image
                            else:
                                counter = counter - 1
                                continue

    def get_text_of_valid_sibling(self, elem):
        elems = elem.next_siblings
        for e in elems:
            try:
                return e.get_text()
            except:
                pass

    def get_no_of_days_of_month_by_url(self, url):
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
