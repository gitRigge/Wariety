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

import datetime
import hashlib
import logging
import os
import random
import sqlite3
import sys
import warnings

import PIL.Image
from pubsub import pub

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
        self.my_queue = wariety_queue.WarietyQueue.instance(self.config)

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

    def push_empty_queue(self):
        """
        Sends 'empty queue' message
        :return:
        """
        logger.debug('push_empty_queue()')
        pub.sendMessage("empty queue", cls=self.my_queue, msg='')

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

            sql = ''
            if self.table_exists(tbl_name):

                # Alter table
                items = my_object.to_dict()
                items_length = len(items)
                counter = 0
                for key, value in items.items():
                    if not self.column_exists(key, tbl_name):
                        _dftl_value = value[1]
                        if _dftl_value == '':
                            _dftl_value = '""'
                        sql = 'ALTER TABLE {0} ADD {1} {2} default {3};'.format(tbl_name, key, value[0], _dftl_value)

            else:

                # Create table
                sql = 'CREATE TABLE IF NOT EXISTS {0} ('.format(tbl_name)
                items = my_object.to_dict()
                items_length = len(items)
                counter = 0
                for key, value in items.items():
                    counter = counter + 1
                    _dftl_value = value[1]
                    if _dftl_value == '':
                        _dftl_value = '""'
                    if counter < items_length:
                        sql = sql + '{0} {1} default {2},'.format(key, value[0], _dftl_value)
                    else:
                        sql = sql + '{0} {1} default {2}'.format(key, value[0], _dftl_value)
                sql = sql + ');'

            try:

                # Create table
                c.execute(sql)

                # Save (commit) the changes
                conn.commit()

            except sqlite3.Error as error:
                logger.debug("Error while working with SQLite", error)

            finally:
                if conn:
                    # Close connection
                    conn.close()

    def table_exists(self, table_name):
        """
        Checks if the table name given by 'table_name' exists in the
        database. If it exists, returns 'True' otherwise 'False'
        :param table_name:
        :return:
        """
        logger.debug('table_exists({})'.format(table_name))

        retval = False

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build query
        sql = 'SELECT name \
                    FROM sqlite_master \
                    WHERE type = ? AND \
                    name = ?'

        try:
            c.execute(sql, ('table', table_name,))

            results = c.fetchall()
            if len(results) > 0:
                if table_name in results[0]:
                    retval = True

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return retval

    def column_exists(self, column_name, table_name):
        """
        Checks if the column name given by 'column_name' exists in the table
        given by 'table_name'. If it exists, returns 'True' otherwise 'False'
        :param column_name:
        :return: retval
        """
        logger.debug('column_exists({}, {})'.format(column_name, table_name))

        retval = False

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Create table
        sql = 'SELECT {} FROM {}'.format(column_name, table_name)
        try:
            c.execute(sql)
            retval = True

        except sqlite3.OperationalError as error:
            retval = False

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return retval

    def set_total_seen_number_by_id(self, wallpaper_id):
        """
        Increases the 'total_seen_number' counter with 1 of the image with
        the ID given by 'wallpaper_id'.
        :param wallpaper_id:
        :return:
        """

        logger.debug('set_total_seen_number_by_id({})'.format(wallpaper_id))

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

    def add_item_to_queue(self, new_queue_item):
        """
        Adds the queue item given by 'new_queue_item' to the database.
        :param new_queue_item:
        :return:
        """
        logger.debug('add_item_to_queue()')

        my_queue = wariety_queue.WarietyQueue.instance()

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build SQL string
        sql = 'INSERT INTO queue ('
        queue_item_items = my_queue.to_dict()
        queue_item_items_length = len(queue_item_items)
        counter = 0
        # Add INSERTs
        for key, value in queue_item_items.items():
            counter = counter + 1
            if key == 'id':
                # Do not insert 'id'
                continue
            elif counter < queue_item_items_length:
                sql = sql + '{0},'.format(key)
            else:
                sql = sql + '{0}'.format(key)
        sql = sql + ') VALUES ('
        queue_item_items = new_queue_item.to_dict()
        queue_item_items_length = len(queue_item_items)
        params = []
        counter = 0
        # Add VALUEs
        for key, value in queue_item_items.items():
            counter = counter + 1
            if key == 'id':
                # Do not insert 'id'
                continue
            elif counter < queue_item_items_length:
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

    def get_queue_id_by_id(self, wallpaper_id):
        """
        Get ID of queued image with image ID given by 'wallpaper_id' and
        status 'QUEUED', if available.
        Otherwise, returns -1
        :param wallpaper_id:
        :return: queued_image_id
        """

        logger.debug('get_queue_id_by_id({})'.format(wallpaper_id))

        queued_image_id = -1

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Queue status
        _status = wariety_queue.WarietyQueue.queue_statuses['QUEUED']

        # Select a row
        sql = 'SELECT id \
                FROM queue \
                WHERE queue_status = ? AND \
                image_id = ?'

        try:
            c.execute(sql, (_status, wallpaper_id,))

            result = c.fetchone()

            queued_image_id = int(result[0])

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return queued_image_id

    def set_previous_seen_by_queue_id(self, queue_id, previous_queue_id):
        """
        Sets previous queue ID to the value given by 'previous_queue_id' of
        the image specified by 'queue_id'
        :param queue_id:
        :param previous_queue_id:
        :return:
        """
        logger.debug('set_previous_seen_by_queue_id({}, {})'.format(queue_id, previous_queue_id))

        # Queue status
        _status = wariety_queue.WarietyQueue.queue_statuses['DONE']
        _now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build SQL string
        sql = 'UPDATE queue SET queue_status = ?, queue_seen_date = ?, previous_queue_id = ? \
            WHERE id = ?'

        try:
            c.execute(sql, (_status, _now, previous_queue_id, queue_id,))

            # Save (commit) the changes
            conn.commit()

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def set_currently_seeing_by_queue_id(self, queue_id):
        """
        Sets queue status of queue item given by 'queue_id' to 'CURRENT'
        and sets queue status to 'DONE' where it was set to 'CURRENT' before
        :param queue_id:
        :return:
        """
        logger.debug('set_currently_seeing_by_queue_id({})'.format(queue_id))

        # Queue status
        _status_crnt = wariety_queue.WarietyQueue.queue_statuses['CURRENT']
        _status_done = wariety_queue.WarietyQueue.queue_statuses['DONE']

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build SQL strings
        sql1 = 'UPDATE queue SET queue_status = ? WHERE queue_status = ?'
        sql2 = 'UPDATE queue SET queue_status = ? WHERE id = ?'

        try:
            c.execute(sql1, (_status_done, _status_crnt,))
            c.execute(sql2, (_status_crnt, queue_id,))

            # Save (commit) the changes
            conn.commit()

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def get_next_images_from_queue(self, number_of_images=1):
        """
        Returns images with the highest queue rank and status 'QUEUED', if available.
        Otherwise, returns empty images with counter -1
        :param number_of_images:
        :return: my_images[]
        """
        logger.debug('get_next_images_from_queue({})'.format(number_of_images))

        # Return values array
        my_images = []

        # Queue status
        _status = wariety_queue.WarietyQueue.queue_statuses['QUEUED']

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        sql = 'SELECT * \
            FROM wallpapers \
            INNER JOIN queue ON wallpapers.id = queue.image_id \
            WHERE queue.queue_status = ? \
            ORDER BY queue.queue_rank DESC \
            LIMIT ?'

        try:
            c.execute(sql, (_status, number_of_images, ))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:
                    # Wallpaper
                    my_image = wariety_wallpaper.WarietyWallpaper()

                    if result is not None:
                        my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
                    else:
                        my_image.found_at_counter = -1
                    my_images.append(my_image)
            else:
                # Wallpaper
                my_image = wariety_wallpaper.WarietyWallpaper()
                my_image.found_at_counter = -1
                my_images.append(my_image)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

    def get_previous_queue_items_by_queue_id(self, queue_id, number_of_items=1):
        """
        Returns queue items which have been seen previously to the image specified by 'queue_id'.
        Returns amount of queue items specified by 'number_of_images'.
        :param queue_id:
        :param number_of_items:
        :return: my_queue_items[]:
        """
        logger.debug('get_previous_images_from_queue_by_queue_id({}, {})'.format(queue_id, number_of_items))

        # Return values array
        my_queue_items = []

        # Seen date of image specified by 'queue_id'
        image_seen_date = self.get_seen_date_by_queue_id(queue_id)

        # Queue status
        _status = wariety_queue.WarietyQueue.queue_statuses['DONE']

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Build SQL string
        sql = 'SELECT * \
                FROM queue \
                WHERE queue_seen_date < ? AND queue_status = ? \
                ORDER BY queue_seen_date DESC \
                LIMIT ?'

        try:
            c.execute(sql, (image_seen_date, _status, number_of_items, ))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:

                    # Queue item
                    my_queue_item = wariety_queue.WarietyQueue.instance()

                    if result is not None:
                        my_queue_item = wariety_queue.to_queue_item(result, wariety_queue.WarietyQueue.instance())
                    else:
                        my_queue_item.id = -1
                    my_queue_items.append(my_queue_item)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_queue_items

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

    def get_total_number_of_images(self, source_table='wallpapers', status='DOWNLOADED'):
        """
        Returns the total number of images of the table given by 'source_table' with the status given
        by 'status'
        :param source_table:
        :param status:
        :return total_number_of_images_in_db:
        """
        logger.debug('get_total_number_of_images({}, {})'.format(source_table, status))

        total_number_of_images_in_db = 0

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # SQL
        sql = ''
        if source_table == 'wallpapers':
            sql = 'SELECT COUNT(id) FROM wallpapers WHERE status = ?'
        elif source_table == 'queue':
            sql = 'SELECT COUNT(wallpapers.id) \
                    FROM wallpapers \
                    INNER JOIN queue ON wallpapers.id = queue.image_id \
                    WHERE queue.queue_status = ?'
        else:
            sql = 'upsi :-)'

        try:
            c.execute(sql, (status, ))

            result = c.fetchone()

            total_number_of_images_in_db = int(result[0])

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return total_number_of_images_in_db

    def get_days_since_last_seen_by_id(self, wallpaper_id):
        """
        Returns the number of days between now and the date when the image given by 'wallpaper_id' has been
        seen the last time. Returns -1 if the image haven't been seen at all.
        :param wallpaper_id:
        :return days_diff:
        """
        logger.debug('get_days_since_last_seen_by_id({})'.format(wallpaper_id))

        _status = wariety_queue.WarietyQueue.queue_statuses['DONE']

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Return value
        days_diff = 0

        # Select a row
        sql = 'SELECT queue.queue_seen_date \
            FROM wallpapers \
            INNER JOIN queue ON wallpapers.id = queue.image_id \
            WHERE queue.queue_status = ? AND wallpapers.id = ? \
            ORDER BY queue.queue_seen_date DESC LIMIT 1;'

        try:
            c.execute(sql, (_status, wallpaper_id, ))

            result = c.fetchone()

            if result is not None:
                _now = datetime.datetime.now()
                _last_seen_date = datetime.datetime.strptime(result[0], "%Y%m%d%H%M%S")
                days_diff = (_now - _last_seen_date).days
            else:
                days_diff = -1

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return days_diff

    def set_last_seen_date_by_queue_id(self, queue_id, last_seen_date='00000000000000'):
        """
        Sets the last seen date given by 'last_seen_date' of the image specified by
        'queue_id'. If no last seen date is given, sets the last seen date to now.
        :param queue_id:
        :param last_seen_date:
        """
        logger.debug('set_last_seen_date_by_queue_id({})'.format(queue_id))

        _last_seen_date = ''

        if last_seen_date == '00000000000000':
            _last_seen_date = datetime.datetime.now()
        else:
            _last_seen_date = datetime.datetime.strptime(last_seen_date, "%Y%m%d%H%M%S")

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Build SQL string
            sql = 'UPDATE queue SET queue_seen_date = ? WHERE id = ?'
            c.execute(sql, (_last_seen_date.strftime("%Y%m%d%H%M%S"),queue_id,))

            # Save (commit) the changes
            conn.commit()

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()

    def get_latest_image(self, number_of_images=1, source_type='*', status='DOWNLOADED'):
        """
        Returns the latest downloaded image(s) at all. Or, if given, returns the latest
        downloaded image(s) of source type given by 'source type'. Returns only downloaded
        images unless other status given as 'status'. Returns -1 if no latest image(s) is
        available.
        :param number_of_images:
        :param source_type:
        :param status:
        :return my_images:
        """
        logger.debug('get_latest_image({}, {}, {})'.format(number_of_images, source_type, status))

        # Return values array
        my_images = []

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Build SQL string
            _now = datetime.datetime.now().strftime("%Y%m%d000000")
            if source_type == '*':
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE download_date >= ? AND status = ? \
                    ORDER BY found_at_counter DESC LIMIT ?'
                c.execute(sql, (_now, status, number_of_images, ))
            else:
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE source_type = ? AND download_date >= ? AND status = ? \
                    ORDER BY found_at_counter DESC LIMIT ?'
                c.execute(sql, (source_type, _now, status, number_of_images, ))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:
                    # Wallpaper
                    my_image = wariety_wallpaper.WarietyWallpaper()

                    if result is not None:
                        my_image = wariety_wallpaper.to_wallpaper(result[0], wariety_wallpaper.WarietyWallpaper())
                    else:
                        my_image.found_at_counter = -1
                    my_images.append(my_image)
            else:
                # Wallpaper
                my_image = wariety_wallpaper.WarietyWallpaper()
                my_image.found_at_counter = -1
                my_images.append(my_image)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

    def get_random_image(self, number_of_images=1, source_type='*', status='DOWNLOADED'):
        """
        Returns random image(s) in the database. If given, returns random image(s) in the
        database of the source type given by 'source_type'. Returns only downloaded images
        unless other status given as 'status'. Returns -1 if no random image(s) is available.
        :param number_of_images:
        :param source_type:
        :param status:
        :return my_images:
        """
        logger.debug('get_random_image({}, {}, {})'.format(number_of_images, source_type, status))

        # Return values array
        my_images = []

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Build SQL string
            if source_type == '*':
                sql = 'SELECT id FROM wallpapers WHERE status = ? ORDER BY id'
                c.execute(sql, (status,))
            else:
                sql = 'SELECT id FROM wallpapers WHERE source_type = ? AND status = ? ORDER BY id'
                c.execute(sql, (source_type, status,))
            result = c.fetchall()

            for i in range(0, number_of_images):
                _max = len(result)
                _choice = random.randint(0, int(_max))
                random_image_id = result[_choice][0]

                # Build SQL string
                sql = 'SELECT * FROM wallpapers WHERE id = ?'
                c.execute(sql, (random_image_id,))
                result = c.fetchone()

                # Wallpaper
                my_image = wariety_wallpaper.WarietyWallpaper()
                if result is not None:
                    my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
                    my_images.append(my_image)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

    def get_oldest_image(self, number_of_images=1, source_type='*', status='DOWNLOADED'):
        """
        Returns the oldest image(s) in the database. If given, returns the oldest image(s)
        in the database of the source type given by 'source_type'. Returns only downloaded
        images unless other status given as 'status'. Returns -1 if no oldest image(s) is
        available.
        :param number_of_images:
        :param source_type:
        :param status:
        :return my_images:
        """
        logger.debug('get_oldest_image({}, {}, {})'.format(number_of_images, source_type, status))

        # Return values array
        my_images = []

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Select a row
            if source_type == '*':
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE status = ? \
                    ORDER BY download_date ASC LIMIT ?'
                c.execute(sql, (status, number_of_images, ))
            else:
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE source_type = ? AND status = ? \
                    ORDER BY download_date ASC LIMIT ?'
                c.execute(sql, (source_type,status, number_of_images, ))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:
                    # Wallpaper
                    my_image = wariety_wallpaper.WarietyWallpaper()
                    if result is not None:
                        my_image = wariety_wallpaper.to_wallpaper(result[0], wariety_wallpaper.WarietyWallpaper())
                    else:
                        my_image.found_at_counter = -1
                    my_images.append(my_image)
            else:
                # Wallpaper
                my_image = wariety_wallpaper.WarietyWallpaper()
                my_image.found_at_counter = -1
                my_images.append(my_image)


        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

    def get_seen_date_by_queue_id(self, queue_id):
        """
        Returns the seen date of the image specified by 'queue_id', if
        available. Otherwise, returns '19700101000000'
        :param queue_id:
        :return: seen_date
        """

        logger.debug('get_seen_date_by_queue_id({})'.format(queue_id))

        seen_date = '19700101000000'

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        sql = 'SELECT queue_seen_date FROM queue WHERE id = ?'

        try:
            c.execute(sql, (queue_id,))

            result = c.fetchone()

            seen_date = str(result[0])

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return seen_date

    def get_seen_image(self, number_of_images=1, seen=0, source_type='*', status='DOWNLOADED'):
        """
        Returns the oldest image(s) in the database which has a total_seen value of 'seen' or less.
        If given, returns the oldest image(s) in the database which has a total_seen value of 'seen'
        or less of the source type given by 'source_type'. Returns only downloaded images unless
        other status given as 'status'. Returns -1 if no seen images are available.
        :param number_of_images:
        :param seen:
        :param source_type:
        :param status:
        :return my_images:
        """
        logger.debug('get_seen_image({}, {}, {})'.format(seen, source_type, status))

        # Return values array
        my_images = []

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Select a row
            if source_type == '*':
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE status = ? AND total_seen_number <= ? \
                    ORDER BY download_date ASC LIMIT ?'
                c.execute(sql, (status, seen, number_of_images, ))
            else:
                sql = 'SELECT * \
                    FROM wallpapers \
                    WHERE source_type = ? AND status = ? AND total_seen_number <= ? \
                    ORDER BY download_date ASC LIMIT ?'
                c.execute(sql, (source_type, status, seen, number_of_images, ))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:
                    # Wallpaper
                    my_image = wariety_wallpaper.WarietyWallpaper()
                    if result is not None:
                        my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
                    else:
                        my_image.found_at_counter = -1
                    my_images.append(my_image)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

    def get_rated_image(self, number_of_images=1, rating=0, source_type='*', status='DOWNLOADED'):
        """
        Returns the oldest images in the database which are rated with rate 'rating' or less. If given,
        returns the oldest images in the database of the source type given by 'source_type' which are
        rated with rate 'rating' or less. Returns only downloaded images unless other status given as
        'status'.  Returns -1 if no rated images are available.
        :param number_of_images:
        :param rating:
        :param source_type:
        :param status:
        :return my_images:
        """
        logger.debug('get_rated_image({}, {}, {}, {})'.format(number_of_images, rating, source_type, status))

        # Return values array
        my_images = []

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Select a row
            if source_type == '*':
                sql = 'SELECT * \
                            FROM wallpapers \
                            WHERE status = ? AND image_rating <= ? \
                            ORDER BY download_date ASC, image_rating DESC LIMIT ?'
                c.execute(sql, (status, rating, number_of_images, ))
            else:
                sql = 'SELECT * \
                            FROM wallpapers \
                            WHERE source_type = ? AND status = ? AND image_rating <= ? \
                            ORDER BY download_date ASC, image_rating DESC LIMIT ?'
                c.execute(sql, (source_type, status, rating, number_of_images, ))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:
                    # Wallpaper
                    my_image = wariety_wallpaper.WarietyWallpaper()
                    if result is not None:
                        my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
                    else:
                        my_image.found_at_counter = -1
                    my_images.append(my_image)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

    def get_most_recent_seen_image(self, number_of_images=1, source_type='*', status='DONE'):
        """
        Returns the most recent seen images in the database. If given, returns the most recent
        seen images in the database of the source type given by 'source_type'. Returns only
        downloaded images unless other status given as 'status'.  Returns -1 if no recent seen
        images are available.
        :param number_of_images:
        :param source_type:
        :param status:
        :return my_images:
        """
        logger.debug('get_most_recent_seen_image({}, {}, {})'.format(number_of_images, source_type, status))

        # Return values array
        my_images = []

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        try:
            # Select a row
            if source_type == '*':
                sql = 'SELECT * \
                        FROM wallpapers \
                        INNER JOIN queue ON wallpapers.id = queue.image_id \
                        WHERE queue.queue_status = ? \
                        ORDER BY queue.queue_seen_date ASC LIMIT 1'
                c.execute(sql, (status,))
            else:
                sql = 'SELECT * \
                        FROM wallpapers \
                        INNER JOIN queue ON wallpapers.id = queue.image_id \
                        WHERE source_type = ? AND queue.queue_status = ? \
                        ORDER BY queue.queue_seen_date ASC LIMIT 1'
                c.execute(sql, (source_type, status,))

            results = c.fetchall()
            if len(results) > 0:
                for result in results:
                    # Wallpaper
                    my_image = wariety_wallpaper.WarietyWallpaper()
                    if result is not None:
                        my_image = wariety_wallpaper.to_wallpaper(result, wariety_wallpaper.WarietyWallpaper())
                    else:
                        my_image.found_at_counter = -1
                    my_images.append(my_image)

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)

        finally:
            if conn:
                # Close connection
                conn.close()
            return my_images

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
            c.execute(sql, (md5_hash_value,))
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

    def get_image_description_by_id(self, wallpaper_id):
        """
        Returns the description of the wallpaper image specified by
        'wallpaper_id'.
        :return image_desc:
        """
        logging.debug('get_image_description_by_id({})'.format(wallpaper_id))

        image_desc = ''

        # Establish connection
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Select a row
        sql = 'SELECT image_author,location,source_name FROM wallpapers WHERE id = ?'

        try:
            c.execute(sql, (wallpaper_id,))
            result = c.fetchone()

            if result[0] != '':
                if image_desc == '':
                    image_desc = 'By {}'.format(result[0])
                else:
                    image_desc = image_desc + ', by {}'.format(result[0])
            if result[1] != '':
                if image_desc == '':
                    image_desc = 'Location: {}'.format(result[1])
                else:
                    image_desc = image_desc + ', location: {}'.format(result[1])
            if result[2] != '':
                if image_desc == '':
                    image_desc = 'Source: {}'.format(result[2])
                else:
                    image_desc = image_desc + ', source: {}'.format(result[2])

        except sqlite3.Error as error:
            logger.debug("Error while working with SQLite", error)
            image_desc = 'No description available'

        finally:
            if conn:
                # Close connection
                conn.close()
            return image_desc
