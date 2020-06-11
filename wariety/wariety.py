#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import gettext
import glob
import locale
import logging
import os
import sys
import time
import wx
import wx.adv
from pubsub import pub

sys.path.insert(1, '../lib')
import wariety_config
import wariety_database
import wariety_downloader
import wariety_manual_fetcher
import wariety_updater

__author__ = "Roland Rickborn (gitRigge)"
__copyright__ = "Copyright (c) 2020 gitRigge"
__version__ = "0.0.3"
__desc__ = "[Description]"
__status__ = "Development"
__url__ = "https://github.com/gitRigge/wariety"
__releasenotes__ = """[version]
    [Notes]
"""
__license__ = """GPL v3 License

Copyright (c) 2020 gitRigge

"""

APP_NAME = 'Wariety'
CONFIGFILE = os.path.join(os.environ['LOCALAPPDATA'], APP_NAME, 'config.ini')

def get_aboutDlg_args():
    __license__ = get_license()
    __desc__ = get_description()
    args = {'version': __version__, 'desc': __desc__, 'url': __url__, 'copyright': __copyright__,
            'license': __license__}
    return args

def get_settingsDlg_args():
    __releasenotes__ = get_release_notes()
    args = {"config_file": CONFIGFILE, 'releasenotes': __releasenotes__}
    return args

class WarietyMain(wx.adv.TaskBarIcon):

    def __init__(self, icons):
        super(WarietyMain, self).__init__()
        self.set_icon()
        self.dbl_clk_delay = 200
        # Event bindings
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_double)
        self.Bind(wx.EVT_TIMER, self.on_left_single)
        # Configuration
        self.myConfig = wariety_config.WarietyConfig(CONFIGFILE)
        # DB initializing
        self.database = wariety_database.WarietyDatabase(self.myConfig.to_dict())
        self.database.database_maintenance()
        self.database.__del__()
        # Messaging
        pub.subscribe(self.update_downloader, "config updated")
        pub.subscribe(self.update_updater, "config updated")
        pub.subscribe(self.update_manual_fetcher, "config updated")
        # Instantiate the wallpaper updater
        if self.myConfig.wallpaper_change:
            self.myUpdater = wariety_updater.WarietyUpdater(self.myConfig.wallpaper_change_interval,
                                                            self.myConfig.to_dict())
        else:
            self.myUpdater = wariety_updater.WarietyUpdater(0, self.myConfig.to_dict())
        # Instantiate the wallpaper downloader
        if self.myConfig.download_wallpaper:
            self.myDownloader = wariety_downloader.WarietyDownloader(self.myConfig.download_wallpaper_interval,
                                                                     self.myConfig.to_dict())
        else:
            self.myDownloader = wariety_downloader.WarietyDownloader(0, self.myConfig.to_dict())
        # Run Observer in any case
        self.myManualFetcher = wariety_manual_fetcher.WarietyManualFetcher(self.myConfig.to_dict())

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, _('Next'), self.on_next)
        create_menu_item(menu, _('Previous'), self.on_previous)
        menu.AppendSeparator()
        create_menu_item(menu, _('Image Name'), self.on_name)
        create_menu_item(menu, _('Image Source'), self.on_source)
        create_menu_item(menu, _('Add to Favorites'), self.on_favorite)
        create_menu_item(menu, _('Delete Image'), self.on_delete)
        menu.AppendSeparator()
        submenu = wx.Menu()
        create_submenu_item(menu, submenu, _('Next'), self.on_next)
        create_submenu_item(menu, submenu, _('Previous'), self.on_previous)
        submenu.AppendSeparator()
        create_submenu_item(menu, submenu, _('Keep Current'), self.on_keep)
        submenu.AppendSeparator()
        create_submenu_item(menu, submenu, _('Show Source'), self.on_show_source)
        create_submenu_item(menu, submenu, _('Google Image Search'), self.on_image_search)
        submenu.AppendSeparator()
        subsubmenu = wx.Menu()
        create_submenu_item(menu, subsubmenu, u'\u2605\u2605\u2605\u2605\u2605', self.on_five_star)
        create_submenu_item(menu, subsubmenu, u'\u2605\u2605\u2605\u2605', self.on_four_star)
        create_submenu_item(menu, subsubmenu, u'\u2605\u2605\u2605', self.on_three_star)
        create_submenu_item(menu, subsubmenu, u'\u2605\u2605', self.on_two_star)
        create_submenu_item(menu, subsubmenu, u'\u2605', self.on_one_star)
        create_submenu_item(menu, subsubmenu, _('No Vote'), self.on_one_star)
        submenu.AppendSubMenu(subsubmenu, _('Vote'))
        menu.AppendSubMenu(submenu, _('Image'))
        menu.AppendSeparator()
        create_menu_item(menu, _('Settings'), self.on_settings)
        create_menu_item(menu, _('About'), self.on_about)
        create_menu_item(menu, _('Quit'), self.on_exit)
        return menu

    def set_icon(self):
        icon = wx.Icon(icons[0])
        self.SetIcon(icon, APP_NAME)

    def on_left_down(self, event):
        self.start_timer()

    def on_left_double(self, event):
        self.stop_timer()
        print(_('Double Click'))

    def on_left_single(self, event):
        self.stop_timer()
        print(_('Single Click'))

    def start_timer(self):
        self.timer1 = wx.Timer(self)
        self.timer1.Start(self.dbl_clk_delay)

    def stop_timer(self):
        self.timer1.Stop()
        del self.timer1

    def on_next(self, event):
        pass

    def on_previous(self, event):
        pass

    def on_keep(self, event):
        pass

    def on_show_source(self, event):
        pass

    def on_image_search(self, event):
        pass

    def on_one_star(self, event):
        pass

    def on_two_star(self, event):
        pass

    def on_three_star(self, event):
        pass

    def on_four_star(self, event):
        pass

    def on_five_star(self, event):
        pass

    def on_name(self, event):
        pass

    def on_source(self, event):
        pass

    def on_favorite(self, event):
        pass

    def on_delete(self, event):
        pass

    def on_settings(self, event):
        top = SettingsDlg(wx.GetApp().TopWindow, id=-1, title=_('{} {}').format(APP_NAME, _('Settings')))
        top.Show()

    def on_about(self, event):
        top = AboutDlg(wx.GetApp().TopWindow, id=-1, title=_('About {}').format(APP_NAME), name=APP_NAME)
        top.Show()

    def animate_icon(self, event):
        myIcons = icons.copy()
        myIcons_copy = myIcons.copy()
        myIcons_copy.reverse()
        myIcons.extend(myIcons_copy)
        for i in myIcons_copy:
            icon = wx.Icon(i)
            self.SetIcon(icon, APP_NAME)

    def show_balloon_msg(self, event, title, msg):
        self.ShowBalloon(title, msg, msec=0, flags=0)

    def on_exit(self, event):
        self.myDownloader.stop()
        self.myUpdater.stop()
        time.sleep(1.5)
        wx.CallAfter(self.Destroy)

    def update_downloader(self, msg):
        logging.debug('update_downloader()')
        self.myDownloader.stop()
        if msg['download_wallpaper']:
            self.myDownloader = wariety_downloader.WarietyDownloader(msg['download_wallpaper_interval'], msg)
        else:
            self.myDownloader = wariety_downloader.WarietyDownloader(0, msg)

    def update_updater(self, msg):
        logging.debug('update_updater()')
        self.myUpdater.stop()
        if msg['wallpaper_change']:
            self.myUpdater = wariety_updater.WarietyUpdater(msg['wallpaper_change_interval'], msg)
        else:
            self.myUpdater = wariety_updater.WarietyUpdater(0, msg)

    def update_manual_fetcher(self, msg):
        logging.debug('update_manual_fetcher()')
        self.myManualFetcher.on_thread_stop()
        self.myManualFetcher = wariety_manual_fetcher.WarietyManualFetcher(msg)

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


def create_submenu_item(menu, submenu, label, func):
    item = wx.MenuItem(submenu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    submenu.Append(item)
    return item


def get_icons():
    icons = []
    if getattr(sys, 'frozen', False):
        print("We're frozen")
        icons_path = sys._MEIPASS + '/data/icons'
        icons = glob.glob(os.path.join(icons_path, '*.ico'))
    else:
        print("We're script")
        icons = glob.glob('data/icons/*.ico')
    return icons


def get_license():
    if getattr(sys, 'frozen', False):
        license_path = os.path.join(sys._MEIPASS, 'LICENSE')
    else:
        license_path = os.path.join('LICENSE')
    with open(license_path, 'r') as license_file:
        license_content = license_file.read()
    return license_content


def get_release_notes():
    if getattr(sys, 'frozen', False):
        release_notes_path = os.path.join(sys._MEIPASS, 'Release Notes.txt')
    else:
        release_notes_path = os.path.join('Release Notes.txt')
    with open(release_notes_path, 'r') as release_notes_file:
        release_notes_content = release_notes_file.read()
    return release_notes_content


def get_description():
    return _(
        "Wariety is a wallpaper manager for Windows systems. It is a clone of the famous Linux application Variety and covers its main functionality.")

def init_logging(log_file=None, append=False, console_loglevel=logging.INFO):
    """Set up logging to file and console."""
    if log_file is not None:
        if append:
            filemode_val = 'a'
        else:
            filemode_val = 'w'
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s",
                            #format='%(asctime)s - %(message)s',
                            # datefmt='%m-%d %H:%M',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_file,
                            filemode=filemode_val)
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(console_loglevel)
    # set a format which is simpler for console use
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s")
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    global LOG
    LOG = logging.getLogger(__name__)

def main(icons):
    app = wx.App()
    WarietyMain(icons)
    app.MainLoop()


if __name__ == '__main__':
    if __status__ == 'Development':
        # Start Debug Logging if our status equals 'Development'
        myname = os.path.basename(__file__).split('.')[0]
        mypath = os.path.abspath(os.path.join(os.environ['LOCALAPPDATA'], APP_NAME))
        os.makedirs(mypath, exist_ok=True)
        fname = os.path.abspath(os.path.join(mypath, '{}.log'.format(myname)))
        if not os.path.isfile(fname):
            open(fname, 'w').close()
        init_logging(log_file=fname, append=False, console_loglevel=logging.DEBUG)

    logging.debug('Starting application')
    from aboutDlg import AboutDlg
    from settingsDlg import SettingsDlg

    current_locale = locale.getdefaultlocale()[0].split("_")[0]
    if getattr(sys, 'frozen', False):
        lang = gettext.translation('wariety', localedir=sys._MEIPASS + '/locale', languages=[current_locale])
    else:
        lang = gettext.translation('wariety', localedir='locale', languages=[current_locale])
    lang.install()
    _ = lang.gettext
    desc = _(
        "Wariety is a wallpaper manager for Windows systems. It is a clone of the famous Linux application Variety and covers its main functionality.")
    icons = get_icons()
    main(icons)
    logging.debug('Stopping application')
