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

import datetime
import hashlib
import logging
import os
import random
import sqlite3
import sys
import warnings

import PIL.Image

import wariety_downloader
import wariety_queue
import wariety_wallpaper

logger = logging.getLogger(__name__)


def is_image_landscape(asset):
    """Checks the orientation of the asset given by 'asset' and returns 'True' if the asset's
    orientation is landscape. Returns 'False' in any other case.
    """
    # Turn of PIL DecompressionBombWarning
    logger.debug('is_image_landscape({})'.format(asset))
    warnings.simplefilter('ignore', PIL.Image.DecompressionBombWarning)

    # Default value
    my_dim = 0

    try:
        im = PIL.Image.open(asset)
        my_dim = im.size
        im.close()
        if (my_dim[0] > 0) and (my_dim[1] > 0):
            # Calculate Width:Height; > 0 == landscape; < 0 == portrait
            if my_dim[0]/my_dim[1] > 1:
                return True
            else:
                return False
        else:
            return False
    except:
        e = sys.exc_info()[0]
        logger.debug('is_image_landscape() - {}'.format(e))


def get_md5_hash_of_file(full_image_path):
    """
    Calculates and returns the MD5 hash value for the file given by 'full_image_path'.
    :param full_image_path:
    :return image_hash_value:
    """
    logger.debug('get_md5_hash_of_file({})'.format(full_image_path))

    image_hash_value = 0

    try:
        hash_md5 = hashlib.md5()
        with open(full_image_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        image_hash_value = hash_md5.hexdigest()
    except FileNotFoundError as error:
        logger.debug("Error while trying to access file", error)

    finally:
        return image_hash_value


def remove_image_file(image_file_path):
    """
    Removes file given by 'image_file_path' from filesystem.
    :param image_file_path:
    :return:
    """
    logger.debug('remove_image_file({})'.format(image_file_path))

    try:
        if os.path.isfile(image_file_path):
            os.remove(image_file_path)
    except:
        e = sys.exc_info()[0]
        logger.debug('is_image_landscape() - {}'.format(e))


def get_all_image_paths_from_folder_by_path(dir_path):
    """
    Reads the folder given by 'dir_path' and returns a list
    of full image paths of all images currently stored there.
    :return:
    """
    logging.debug('get_all_images_from_filesystem()')

    all_full_image_paths = []
    for my_file in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, my_file)):
            all_full_image_paths.append(os.path.join(dir_path, my_file))
            all_full_image_paths.append(os.path.join(dir_path, my_file))
    return all_full_image_paths


def get_empty_image():
    """
    Returns an empty wallpaper object.
    :return: my_image:
    """
    logger.debug('get_empty_image()')

    # Wallpaper
    my_image = wariety_wallpaper.WarietyWallpaper()

    return my_image


class WarietyDatabase(object):
    """docstring for WarietyDatabase"""

    def __init__(self, config={}):
        logger.debug('Starting DB')
        logger.debug('__init__()')
        self.config = config

        # DB settings
        dir_path = os.path.join(os.environ['LOCALAPPDATA'],'Wariety')  # TODO Replace static string 'Wariety'
        try:
            os.makedirs(dir_path, exist_ok=True)
            self.db_file = os.path.join(dir_path,'wariety.db')
        except:
            e = sys.exc_info()[0]
            logger.debug('__init__() - {}'.format(e))

    def __del__(self):
        logger.debug('__del__()')
        logger.debug('Stopping DB')

    def create_or_alter_tables(self):
        """
        Creates the tables 'wallpapers' and 'queue' if it does not yet exist.
        Otherwise, alters the existing table by creating a new one,
        copying all data and removing the existing one.
        :return:
        """
        logger.debug('create_or_alter_table()')

        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()

        # Queue
        my_queue = wariety_queue.WarietyQueue.instance()

        # Objects
        objects = {'wallpapers': my_image, 'queue': my_queue}

        # Build SQL string
        for obj in objects:

            tbl_name = obj
            my_object = objects[obj]

            # Establish connection
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()

            sql = 'CREATE TABLE IF NOT EXISTS {0} ('.format(tbl_name)
            items = my_object.to_dict()
            items_length = len(items)
            counter = 0
            for key, value in items.items():
                counter = counter + 1
                if counter < items_length:
                    sql = sql + '{0} {1},'.format(key, value[0])
                else:
                    sql = sql + '{0} {1}'.format(key, value[0])
            sql = sql + ');'

            try:

                # Create table
                c.execute(sql)

                # Save (commit) the changes
                conn.commit()

            except sqlite3.Error as error:
                logger.debug("Error while working with SQLite", error)

            counter = 0
            for key, value in items.items():
                if not self.column_exists(key):
                    _dftl_value = value[1]
                    if _dftl_value == '':
                        _dftl_value = '""'
                    sql = 'ALTER TABLE {0} ADD {1} {2} default {3};'.format(tbl_name, key, value[0], _dftl_value)

            try:

                # Alter table
                c.execute(sql)

                # Save (commit) the changes
                conn.commit()

            except sqlite3.Error as error:
                logger.debug("Error while working with SQLite", error)

            finally:
                if conn:
                    # Close connection
                    conn.close()

    def column_exists(self, column_name):
        """
        Checks if the a column name given by 'column_name' exists in the table
        'wallpapers'. If it exists, returns 'True' otherwise 'False'
        :param column_name:
        :return:
        """
        logger.debug('column_exists({})'.format(column_name))

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create table
        sql = 'SELECT {} FROM wallpapers'.format(column_name)
        try:
            c.execute(sql)
            return True

        except sqlite3.OperationalError as error:
            return False

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def set_total_seen_number(self, wallpaper_id):
        """
        Increases the 'total_seen_number' counter with 1 of the image with
        the ID given by 'wallpaper_id'.
        :param wallpaper_id:
        :return:
        """

        logger.debug('set_total_seen_number({})'.format(wallpaper_id))

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build SQL string
        sql = 'UPDATE wallpapers SET total_seen_number = total_seen_number + 1 WHERE id = ?'

        try:
            c.execute(sql, (wallpaper_id, ))

            # Save (commit) the changes
            conn.commit()

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def set_seen_date(self, wallpaper_id):
        logger.debug('set_seen_date({})'.format(wallpaper_id))
        pass

    def add_image_to_database(self, new_wallpaper):
        """
        Adds the wallpaper image given by 'new_wallpaper' to
        the database.
        :param new_wallpaper:
        :return:
        """
        logger.debug('add_image_to_database()')

        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()
        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build SQL string
        sql = 'INSERT INTO wallpapers ('
        wallpaper_items = my_image.to_dict()
        wallpaper_items_length = len(wallpaper_items)
        counter = 0
        # Add INSERTs
        for key, value in wallpaper_items.items():
            counter = counter + 1
            if key == 'id':
                # Do not insert 'id'
                continue
            elif counter < wallpaper_items_length:
                sql = sql + '{0},'.format(key)
            else:
                sql = sql + '{0}'.format(key)
        sql = sql + ') VALUES ('
        new_wallpaper_items = new_wallpaper.to_dict()
        new_wallpaper_items_length = len(new_wallpaper_items)
        params = []
        counter = 0
        # Add VALUEs
        for key, value in new_wallpaper_items.items():
            counter = counter + 1
            if key == 'id':
                # Do not insert 'id'
                continue
            elif key == 'download_date' and counter < new_wallpaper_items_length:
                sql = sql + '?,'
                params.append(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            elif key == 'download_date' and counter == new_wallpaper_items_length:
                sql = sql + '?'
                params.append(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            elif key == 'status' and counter < new_wallpaper_items_length:
                sql = sql + '?,'
                params.append(wariety_wallpaper.WarietyWallpaper().wallpaper_statuses['DOWNLOADED'])
            elif key == 'status' and counter == new_wallpaper_items_length:
                sql = sql + '?'
                params.append(wariety_wallpaper.WarietyWallpaper().wallpaper_statuses['DOWNLOADED'])
            elif counter < new_wallpaper_items_length:
                sql = sql + '?,'
                params.append(value[1])
            else:
                sql = sql + '?'
                params.append(value[1])
        sql = sql + ');'

        try:
            c.execute(sql, tuple(params))
            
            # Save (commit) the changes
            conn.commit()

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def remove_image_by_id(self, wallpaper_id):
        """
        Removes the wallpaper image given by 'remove_wallpaper_id' from
        the database.
        :param wallpaper_id:
        :return:
        """
        logger.debug('remove_image_by_id({})'.format(wallpaper_id))

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Define status
        status = wariety_wallpaper.WarietyWallpaper().wallpaper_statuses['DELETED']

        # Select a row
        sql = 'UPDATE wallpapers SET status = ? WHERE id = ?'

        try:
            c.execute(sql, (status, wallpaper_id,))

            # Save (commit) the changes
            conn.commit()

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def get_image_by_id(self, wallpaper_id):
        """
        Returns the wallpaper image given by 'wallpaper_id' from
        the database.
        :param wallpaper_id:
        :return my_image:
        """
        logger.debug('get_image_by_id({})'.format(wallpaper_id))

        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        sql = 'SELECT * FROM wallpapers WHERE id = ?'

        try:
            c.execute(sql, (wallpaper_id,))

            result = c.fetchone()

            if result is not None:
                my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
            else:
                my_image.found_at_counter = -1

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_image

    def get_latest_image(self, source_type='*', status='DOWNLOADED'):
        """
        Returns the latest downloaded image at all. Or, if given, returns the
        latest downloaded image of source type given by 'source type'. Returns
        only downloaded images unless other status given as 'status'. Returns
        -1 if no latest image is available.
        :param source_type:
        :param status:
        :return: my_image:
        """
        logger.debug('get_latest_image({}, {})'.format(source_type, status))
        
        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Build SQL string
            if source_type == '*':
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE download_date >= ? AND status = ? \
                    ORDER BY found_at_counter DESC LIMIT 1'
                c.execute(sql, (datetime.datetime.now().strftime("%Y%m%d000000"), status, ))
            else:
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE source_type = ? AND download_date >= ? AND status = ? \
                    ORDER BY found_at_counter DESC LIMIT 1'
                c.execute(sql, (source_type,datetime.datetime.now().strftime("%Y%m%d000000"), status, ))

            result = c.fetchone()

            if result is not None:
                my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
            else:
                my_image.found_at_counter = -1

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_image

    def get_random_image(self, source_type='*', status='DOWNLOADED'):
        """
        Returns a random image in the database. If given, returns a random
        image in the database of the source type given by 'source_type'. Returns
        only downloaded images unless other status given as 'status'. Returns
        -1 if no random image is available.
        :param source_type:
        :param status:
        :return: my_image:
        """
        logger.debug('get_latest_image({}, {})'.format(source_type, status))

        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Build SQL string
            if source_type == '*':
                sql = 'SELECT id FROM wallpapers WHERE status = ? ORDER BY id'
                c.execute(sql, (status,))
            else:
                sql = 'SELECT id FROM wallpapers WHERE WHERE source_type = ? AND status = ? ORDER BY id'
                c.execute(sql, (source_type, status,))
            result = c.fetchall()

            _max = len(result)
            _choice = random.randint(0, int(_max + _max * .5))
            random_image_id = result[_choice][0]

            # Build SQL string
            sql = 'SELECT * FROM wallpapers WHERE id = ?'
            c.execute(sql, (random_image_id,))
            result = c.fetchone()

            if result is not None:
                my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
            else:
                my_image.found_at_counter = -1

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_image

    def get_oldest_image(self, source_type='*', status='DOWNLOADED'):
        """
        Returns the oldest image in the database. If given, returns the oldest
        image in the database of the source type given by 'source_type'. Returns
        only downloaded images unless other status given as 'status'. Returns
        -1 if no oldest image is available.
        :param source_type:
        :param status:
        :return: my_image:
        """
        logger.debug('get_oldest_image({}, {})'.format(source_type, status))

        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Select a row
            if source_type == '*':
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE status = ? \
                    ORDER BY download_date ASC LIMIT 1'
                c.execute(sql, (status, ))
            else:
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE source_type = ? AND status = ? \
                    ORDER BY download_date ASC LIMIT 1'
                c.execute(sql, (source_type,status, ))

            result = c.fetchone()

            if result is not None:
                my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
            else:
                my_image.found_at_counter = -1

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_image

    def get_unseen_image(self, source_type='*', status='DOWNLOADED'):
        """
        Returns the oldest unseen image in the database.
        If given, returns the oldest unseen image in the database
        of the source type given by 'source_type'. Returns
        only downloaded images unless other status given as 'status'.
        :param source_type:
        :param status:
        :return my_image:
        """
        logger.debug('get_unseen_image({}, {})'.format(source_type, status))

        # Wallpaper
        my_image = wariety_wallpaper.WarietyWallpaper()

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Select a row
            if source_type == '*':
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE status = ? AND total_seen_number = 0 \
                    ORDER BY download_date ASC LIMIT 1'
                c.execute(sql, (status,))
            else:
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE source_type = ? AND status = ? AND total_seen_number = 0 \
                    ORDER BY download_date ASC LIMIT 1'
                c.execute(sql, (source_type, status,))

            result = c.fetchone()
            my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_image

    def exists_image_by_md5_hash(self, md5_hash_value):
        """
        Checks whether an image given by 'md5_hash_value' exists already in database
        independent whether status is 'DOWNLOADED' or 'DELETED'. Returns image ID if
        image exists. Otherwise, returns '0'.
        :param md5_hash_value:
        :return image_id:
        """
        # Default values
        image_id = 0

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        sql = 'SELECT id FROM wallpapers WHERE image_md5_hash = ?'

        try:
            c.execute(sql, (md5_hash_value))
            result = c.fetchone()

            if result is not None:
                image_id = int(result[0])
            else:
                image_id = 0

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return image_id

    def exists_image_by_url_or_path(self, full_image_url_or_path):
        """
        Checks whether an image given by 'full_image_url' exists already in database
        independent whether status is 'DOWNLOADED' or 'DELETED'. Returns image ID if
        image exists. Otherwise, returns '0'.
        :param full_image_url_or_path:
        :return: image_id:
        """
        logger.debug('exists_image_by_url_or_path({})'.format(full_image_url_or_path))
        
        # Default value
        image_id = 0

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        _i = full_image_url_or_path
        sql = 'SELECT id FROM wallpapers WHERE image_url LIKE ? OR image_path LIKE ?'

        try:
            c.execute(sql, (_i, _i))
            result = c.fetchone()

            if result is not None:
                image_id = int(result[0])
            else:
                image_id = 0

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return image_id

    def database_maintenance(self):
        """
        Keep database and image folder synced and ensure all tables
        are available and have correct name.
        :return:
        """
        logging.debug('database_maintenance()')

        # Ensure correct tables
        self.create_or_alter_tables()

        # Check synced database
        all_images = self.get_all_image_ids_and_paths_from_database()
        for image_id in all_images:
            if not os.path.isfile(all_images[image_id]):
                self.remove_image_by_id(image_id)
                logging.debug('database_maintenance() - image not in folder, deleted')

        # Check temporary folder
        dir_path = self.config['download_wallpaper_folder']
        all_image_file_paths = get_all_image_paths_from_folder_by_path(dir_path)
        for image_file_path in all_image_file_paths:
            image_id = self.exists_image_by_url_or_path(image_file_path)
            if not image_id:
                remove_image_file(image_file_path)
                logging.debug('database_maintenance() - image not in database, deleted')

        # Delete images with wrong orientation
        if wariety_downloader.is_screen_landscape():
            my_orientation = 'landscape'
        else:
            my_orientation = 'portrait'
        all_images = self.get_all_image_ids_and_paths_from_database()
        for image_id in all_images:
            my_image = self.get_image_by_id(image_id)
            if not my_image.image_orientation == my_orientation:
                self.remove_image_by_id(image_id)
                remove_image_file(my_image.image_path)
                logging.debug('database_maintenance() - wrong orientation, deleted')

    def get_all_image_ids_and_paths_from_database(self):
        """
        Reads database and returns dictionary with IDs and full image path of all
        images currently stored in the database with status 'DOWNLOADED'.
        :return all_images:
        """
        logging.debug('get_all_images_from_database()')

        all_images = {}

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        sql = 'SELECT id, image_path FROM wallpapers WHERE status = ?'

        try:
            c.execute(sql, (wariety_wallpaper.WarietyWallpaper().wallpaper_statuses['DOWNLOADED'],))
            result = c.fetchall()

            for item in result:
                all_images[item[0]] = item[1]

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
                return all_images
