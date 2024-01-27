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

#
# generated by wxGlade 0.9.4 on Fri Nov  8 15:37:20 2019
#

# begin wxGlade: dependencies
import gettext
import locale
import logging
import os
import re
import sys

import wx
import wx.adv
from pubsub import pub

# end wxGlade
# begin wxGlade: extracode
# end wxGlade

logger = logging.getLogger(__name__)

current_locale = locale.getdefaultlocale()[0].split("_")[0]
if getattr(sys, 'frozen', False):
    import wariety.wariety as wariety
    import lib.wariety_config
    import lib.wariety_app_updater
    lang = gettext.translation('settingsDlg', localedir=sys._MEIPASS+'/locale', languages=[current_locale])
else:
    import wariety
    import lib.wariety_config
    import lib.wariety_app_updater
    lang = gettext.translation('settingsDlg', localedir='locale', languages=[current_locale])
lang.install()
_ = lang.gettext


class SourcesListCtrl(wx.ListCtrl):
    ''' This is a ListCtrl which add a checkbox in the first column of each row. '''
    def __init__(self, parent, *args, **kwds):
        logger.debug('__init__()')
        wx.ListCtrl.__init__(self, parent, *args, **kwds)


class SettingsDlg(wx.Frame):
    def __init__(self, *args, **kwds):
        logger.debug('__init__()')
        # begin wxGlade: SettingsDlg.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_NO_TASKBAR | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((800, 500))
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_1_General = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.label_5 = wx.StaticText(self.notebook_1_General, wx.ID_ANY, _("General Settings"))
        self.checkbox_6 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Start Wariety automatically with Windows startup\n"))
        self.checkbox_7 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Change wallpaper every"))
        self.combo_box_4 = wx.ComboBox(self.notebook_1_General, wx.ID_ANY, choices=[_("2"), _("4"), _("8"), _("16"), _("32"), _("64"), _("128"), _("256")], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.label_6 = wx.StaticText(self.notebook_1_General, wx.ID_ANY, _("Minutes"))
        self.checkbox_8 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Change wallpaper on Windows startup"))
        self.checkbox_9 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Download a new wallpaper image every"))
        self.combo_box_5 = wx.ComboBox(self.notebook_1_General, wx.ID_ANY, choices=[_("2"), _("4"), _("8"), _("16"), _("32"), _("64"), _("128"), _("256")], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.label_7 = wx.StaticText(self.notebook_1_General, wx.ID_ANY, _("Minutes into the folder"))
        self.dirpickerctrl_1 = wx.DirPickerCtrl(self.notebook_1_General, wx.ID_ANY, style=wx.DIRP_DIR_MUST_EXIST | wx.DIRP_USE_TEXTCTRL | wx.DIRP_SMALL)
        self.checkbox_10 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Limit download folder size to"))
        self.combo_box_6 = wx.ComboBox(self.notebook_1_General, wx.ID_ANY, choices=[_("2"), _("4"), _("8"), _("16"), _("32"), _("64"), _("128"), _("256"), _("512")], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.label_8 = wx.StaticText(self.notebook_1_General, wx.ID_ANY, _("MB (older files are deleted if necessary)"))
        self.checkbox_12 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Animate system tray icon on every wallpaper change"))
        self.checkbox_11 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Show balloon message on every wallpaper change"))
        self.checkbox_3 = wx.CheckBox(self.notebook_1_General, wx.ID_ANY, _("Check for updates on startup"))
        self.panel_3 = wx.Panel(self.notebook_1_General, wx.ID_ANY)
        self.notebook_1_Source = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.label_1 = wx.StaticText(self.notebook_1_Source, wx.ID_ANY, _("Image Sources"))
        self.sources_list_ctrl_1 = SourcesListCtrl(self.notebook_1_Source, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_AUTOARRANGE)
        self.notebook_1_Proxy = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.label_12 = wx.StaticText(self.notebook_1_Proxy, wx.ID_ANY, _("Proxy Settings"))
        self.checkbox_2 = wx.CheckBox(self.notebook_1_Proxy, wx.ID_ANY, _("Use a proxy to download images"))
        self.label_13 = wx.StaticText(self.notebook_1_Proxy, wx.ID_ANY, _("Enter the host or address of the proxy"))
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_1_Proxy, wx.ID_ANY, "")
        self.label_14 = wx.StaticText(self.notebook_1_Proxy, wx.ID_ANY, _("Enter the port of the proxy"))
        self.text_ctrl_5 = wx.TextCtrl(self.notebook_1_Proxy, wx.ID_ANY, "")
        self.label_15 = wx.StaticText(self.notebook_1_Proxy, wx.ID_ANY, _("Enter the username for the proxy"))
        self.text_ctrl_4 = wx.TextCtrl(self.notebook_1_Proxy, wx.ID_ANY, "")
        self.label_16 = wx.StaticText(self.notebook_1_Proxy, wx.ID_ANY, _("Enter the password for the proxy"))
        self.text_ctrl_3 = wx.TextCtrl(self.notebook_1_Proxy, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.panel_4 = wx.Panel(self.notebook_1_Proxy, wx.ID_ANY)
        self.notebook_1_Sync = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.label_2 = wx.StaticText(self.notebook_1_Sync, wx.ID_ANY, _("VRTY.ORG is currently not publically available"))
        self.notebook_1_Fetch = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.label_3 = wx.StaticText(self.notebook_1_Fetch, wx.ID_ANY, _("Manual Download Settings"))
        self.checkbox_1 = wx.CheckBox(self.notebook_1_Fetch, wx.ID_ANY, _("Fetch wallpapers from manual download folder"))
        self.dirpickerctrl_2 = wx.DirPickerCtrl(self.notebook_1_Fetch, wx.ID_ANY, style=wx.DIRP_DIR_MUST_EXIST | wx.DIRP_USE_TEXTCTRL | wx.DIRP_SMALL)
        self.panel_1 = wx.Panel(self.notebook_1_Fetch, wx.ID_ANY)
        self.notebook_1_Info = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.label_4 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Recent changes"))
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_Info, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.label_17 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Check for new version"))
        self.button_2 = wx.Button(self.notebook_1_Info, wx.ID_ANY, _("Check now..."))
        self.label_18 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Latest version is:"))
        self.label_19 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("0.0.0"))
        self.label_9 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Visit project page"))
        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self.notebook_1_Info, wx.ID_ANY, _("https://github.com/gitRigge/wariety"), _("https://github.com/gitRigge/wariety"))
        self.label_10 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Bug report / issue tracker"))
        self.hyperlink_2 = wx.adv.HyperlinkCtrl(self.notebook_1_Info, wx.ID_ANY, _("https://github.com/gitRigge/wariety/issues"), _("https://github.com/gitRigge/wariety/issues"))
        self.label_11 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Change requests"))
        self.hyperlink_3 = wx.adv.HyperlinkCtrl(self.notebook_1_Info, wx.ID_ANY, _("https://github.com/gitRigge/wariety/pulls"), _("https://github.com/gitRigge/wariety/pulls"))
        self.button_1 = wx.Button(self, wx.ID_ANY, _("Close"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_6, self.checkbox_6)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_7, self.checkbox_7)
        self.Bind(wx.EVT_COMBOBOX, self.OnClicked, self.combo_box_4)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_8, self.checkbox_8)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_9, self.checkbox_9)
        self.Bind(wx.EVT_COMBOBOX, self.OnClicked, self.combo_box_5)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_10, self.checkbox_10)
        self.Bind(wx.EVT_COMBOBOX, self.OnClicked, self.combo_box_6)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_12, self.checkbox_12)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_11, self.checkbox_11)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_3, self.checkbox_3)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_2, self.checkbox_2)
        self.Bind(wx.EVT_TEXT, self.OnTextTextCtrl_2, self.text_ctrl_2)
        self.Bind(wx.EVT_TEXT, self.OnTextTextCtrl_5, self.text_ctrl_5)
        self.Bind(wx.EVT_TEXT, self.OnTextTextCtrl_4, self.text_ctrl_4)
        self.Bind(wx.EVT_TEXT, self.OnTextTextCtrl_3, self.text_ctrl_3)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_1, self.checkbox_1)
        self.Bind(wx.EVT_TEXT, self.OnTextTextCtrl_1, self.text_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1, self.button_1)
        # end wxGlade
        self.sources_list_ctrl_1.EnableCheckBoxes(True)
        self.sources_list_items_1 = {}
        title = kwds.get('title', 'Wariety Settings')
        self.set_properties_received_by_main(title)
        self.myConfig = lib.wariety_config.WarietyConfig(self.config_file)
        self.set_settings()
        # Bind events _after_ adding items
        self.Bind(wx.EVT_CLOSE, self.OnButton_1)
        self.Bind(wx.EVT_LIST_ITEM_CHECKED, self.OnClickedListCheckbox, self.sources_list_ctrl_1)
        self.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.OnClickedListCheckbox, self.sources_list_ctrl_1)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnClickedListCheckbox, self.sources_list_ctrl_1)
        # Important: call the Centre method that centers automatically the window for you
        self.Centre()

        # Messaging
        pub.subscribe(self.show_version_str, "show version str")

    def set_properties_received_by_main(self, title):
        logger.debug('set_properties_received_by_main()')
        args = wariety.get_settingsDlg_args()
        self.config_file = args['config_file']
        self.releasenotes = args['releasenotes']
        self.SetTitle(title)

    def save_settings(self):
        logger.debug('save_settings()')

        # General
        self.myConfig.start_at_startup = self.checkbox_6.GetValue()
        self.myConfig.wallpaper_change = self.checkbox_7.GetValue()
        self.myConfig.wallpaper_change_interval = self.combo_box_4.GetString(self.combo_box_4.GetSelection())
        self.myConfig.change_wallpaper_at_startup = self.checkbox_8.GetValue()
        self.myConfig.download_wallpaper = self.checkbox_9.GetValue()
        self.myConfig.download_wallpaper_interval = self.combo_box_5.GetString(self.combo_box_5.GetSelection())
        self.myConfig.download_wallpaper_folder = self.dirpickerctrl_1.GetPath()
        self.myConfig.max_wallpaper_folder = self.checkbox_10.GetValue()
        self.myConfig.max_wallpaper_folder_size = self.combo_box_6.GetString(self.combo_box_6.GetSelection())
        self.myConfig.manual_download = self.checkbox_1.GetValue()
        self.myConfig.manual_download_folder = self.dirpickerctrl_2.GetPath()
        self.myConfig.animate_system_tray_icon = self.checkbox_12.GetValue()
        self.myConfig.show_balloon_message = self.checkbox_11.GetValue()
        self.myConfig.update_check = self.checkbox_3.GetValue()

        # Proxy
        self.myConfig.proxy_enable = self.checkbox_2.GetValue()
        _host = self.text_ctrl_2.GetValue()
        if _host != '':
            self.myConfig.proxy_address = _host
            try:
                self.myConfig.proxy_port = int(self.text_ctrl_5.GetValue())
            except:
                logger.debug('save_settings() - No integer')
                self.myConfig.proxy_port = 0
            self.myConfig.proxy_username = self.text_ctrl_4.GetValue()
            self.myConfig.proxy_pw_encrypted = self.text_ctrl_3.GetValue()
        else:
            self.myConfig.proxy_enable = False
            self.myConfig.proxy_address = ''
            self.myConfig.proxy_port = 0
            self.myConfig.proxy_username = ''
            self.myConfig.proxy_pw_encrypted = ''

        # Sources
        counter = 0
        for dl in self.myConfig.builtin_downloaders:
            item = self.sources_list_ctrl_1.GetItem(counter)
            try:
                self.myConfig.builtin_downloaders[dl] = self.sources_list_ctrl_1.IsItemChecked(item.GetId())
            except:
                logger.debug('save_settings() - No item of internal downloaders list')
                self.myConfig.external_downloaders[dl] = False
            counter += 1

        # External sources
        for dl in self.myConfig.external_downloaders:
            item = self.sources_list_ctrl_1.GetItem(counter)
            try:
                self.myConfig.external_downloaders[dl] = self.sources_list_ctrl_1.IsItemChecked(item.GetId())
            except:
                logger.debug('save_settings() - No item of external downloaders list')
                self.myConfig.external_downloaders[dl] = False
            counter += 1

    def set_settings(self):
        logger.debug('set_settings()')

        # General
        self.checkbox_6.SetValue(self.myConfig.start_at_startup)
        self.checkbox_7.SetValue(self.myConfig.wallpaper_change)
        if self.myConfig.wallpaper_change == False:
            self.disble_Checkbox_7()
        self.combo_box_4.SetSelection(self.combo_box_4.FindString(str(self.myConfig.wallpaper_change_interval)))
        self.checkbox_8.SetValue(self.myConfig.change_wallpaper_at_startup)
        self.checkbox_9.SetValue(self.myConfig.download_wallpaper)
        if self.myConfig.download_wallpaper == False:
            self.disble_Checkbox_9()
        self.combo_box_5.SetSelection(self.combo_box_5.FindString(str(self.myConfig.download_wallpaper_interval)))
        self.dirpickerctrl_1.SetPath(self.myConfig.download_wallpaper_folder)
        self.checkbox_10.SetValue(self.myConfig.max_wallpaper_folder)
        if self.myConfig.max_wallpaper_folder == False:
            self.disble_Checkbox_10()
        self.combo_box_6.SetSelection(self.combo_box_6.FindString(str(self.myConfig.max_wallpaper_folder_size)))
        self.checkbox_1.SetValue(self.myConfig.manual_download)
        if self.myConfig.manual_download == False:
            self.disable_Checkbox_1()
        self.dirpickerctrl_2.SetPath(self.myConfig.manual_download_folder)
        self.checkbox_12.SetValue(self.myConfig.animate_system_tray_icon)
        self.checkbox_11.SetValue(self.myConfig.show_balloon_message)
        self.checkbox_3.SetValue(self.myConfig.update_check)

        # Proxy
        if self.myConfig.proxy_enable == False:
            self.disable_proxy_settings()
        else:
            self.enable_proxy_settings()
            self.checkbox_2.SetValue(self.myConfig.proxy_enable)
            self.text_ctrl_2.ChangeValue(self.myConfig.proxy_address)
            self.text_ctrl_5.ChangeValue(str(self.myConfig.proxy_port))
            self.text_ctrl_4.ChangeValue(self.myConfig.proxy_username)
            self.text_ctrl_3.ChangeValue(self.myConfig.proxy_pw_encrypted)

        # Basic Columns Definition and Width
        self.sources_list_ctrl_1.InsertColumn(0, _("Activated"), wx.LIST_FORMAT_CENTRE)
        self.sources_list_ctrl_1.InsertColumn(1, _("Type"))
        self.sources_list_ctrl_1.InsertColumn(2, _("Source"))
        self.sources_list_ctrl_1.SetColumnWidth(0, 70)
        self.sources_list_ctrl_1.SetColumnWidth(1, 200)
        self.sources_list_ctrl_1.SetColumnWidth(2, 480)

        # Built-in Downloaders
        counter = 0
        for dl in self.myConfig.builtin_downloaders:
            _desc = self.myConfig.available_builtin_downloaders[dl][0]  # TODO can be better solved than [0]
            _base_url = self.myConfig.available_builtin_downloaders[dl][2]
            _state = self.myConfig.builtin_downloaders[dl]
            index = self.sources_list_ctrl_1.InsertItem(counter, "")
            self.sources_list_ctrl_1.SetItem(index, 1, _desc)
            self.sources_list_ctrl_1.SetItem(index, 2, _base_url)
            self.sources_list_ctrl_1.SetItemData(index, counter)
            if _state:
                self.sources_list_ctrl_1.CheckItem(index, check=True)
            else:
                self.sources_list_ctrl_1.CheckItem(index, check=False)
            counter += 1

        # External Downloaders
        for dl in self.myConfig.external_downloaders:
            _desc = self.myConfig.available_external_downloaders[dl][0]  # TODO can be better solved than [0]
            _base_url = self.myConfig.available_external_downloaders[dl][2]
            _state = self.myConfig.external_downloaders[dl]
            index = self.sources_list_ctrl_1.InsertItem(sys.maxsize, "")
            self.sources_list_ctrl_1.SetItem(index, 1, _desc)
            self.sources_list_ctrl_1.SetItem(index, 2, _base_url)
            self.sources_list_ctrl_1.SetItemData(index, counter)
            if _state:
                self.sources_list_ctrl_1.CheckItem(index, check=True)
            else:
                self.sources_list_ctrl_1.CheckItem(index, check=False)
            counter += 1

        self.text_ctrl_1.SetValue(self.releasenotes)

    def __set_properties(self):
        logger.debug('__set_properties()')
        # begin wxGlade: SettingsDlg.__set_properties
        self.SetTitle(_("Wariety Settings"))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.label_5.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.dirpickerctrl_1.SetMinSize((-1, 23))
        self.notebook_1_General.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.label_1.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.label_12.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.text_ctrl_2.SetMinSize((400, -1))
        self.text_ctrl_5.SetMinSize((400, -1))
        self.text_ctrl_4.SetMinSize((400, -1))
        self.text_ctrl_3.SetMinSize((400, -1))
        self.notebook_1_Sync.Enable(False)
        self.label_3.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.dirpickerctrl_2.SetMinSize((-1, 23))
        self.label_4.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.text_ctrl_1.SetMinSize((760, 100))
        self.label_17.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.label_19.Enable(False)
        self.label_9.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.label_10.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.label_11.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.notebook_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.button_1.SetToolTip(_("Hit button to save and close"))
        self.button_1.SetFocus()
        # end wxGlade
        if getattr(sys, 'frozen', False):
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap(sys._MEIPASS+'/data/icons/logo_1_32x32px.ico', wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
        else:
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap('data/icons/logo_1_32x32px.ico', wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)

    def __do_layout(self):
        logger.debug('__do_layout()')
        # begin wxGlade: SettingsDlg.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(4, 2, 0, 0)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.FlexGridSizer(7, 2, 0, 0)
        self.sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.label_5, 0, wx.ALL, 10)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_4.Add(self.checkbox_6, 0, wx.ALL, 10)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.checkbox_7, 0, wx.ALL, 10)
        sizer_5.Add(self.combo_box_4, 0, wx.ALL, 6)
        sizer_5.Add(self.label_6, 0, wx.ALL, 10)
        sizer_2.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.checkbox_8, 0, wx.ALL, 10)
        sizer_2.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_7.Add(self.checkbox_9, 0, wx.ALL, 10)
        sizer_7.Add(self.combo_box_5, 0, wx.ALL, 6)
        sizer_7.Add(self.label_7, 0, wx.ALL, 10)
        sizer_7.Add(self.dirpickerctrl_1, 1, wx.ALL | wx.EXPAND, 0)
        sizer_2.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_8.Add(self.checkbox_10, 0, wx.ALL, 10)
        sizer_8.Add(self.combo_box_6, 0, wx.ALL, 6)
        sizer_8.Add(self.label_8, 0, wx.ALL, 10)
        sizer_2.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_2.Add(self.checkbox_12, 0, wx.ALL, 10)
        sizer_2.Add(self.checkbox_11, 0, wx.ALL, 10)
        sizer_2.Add(self.checkbox_3, 0, wx.ALL, 10)
        sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)
        self.notebook_1_General.SetSizer(sizer_2)
        self.sizer_9.Add(self.label_1, 0, wx.ALL, 10)
        self.sizer_9.Add(self.sources_list_ctrl_1, 1, wx.EXPAND, 0)
        self.notebook_1_Source.SetSizer(self.sizer_9)
        sizer_14.Add(self.label_12, 0, wx.ALL, 10)
        sizer_14.Add((0, 0), 0, 0, 0)
        sizer_14.Add(self.checkbox_2, 0, wx.ALL, 10)
        sizer_14.Add((0, 0), 0, 0, 0)
        sizer_14.Add(self.label_13, 0, wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_2, 0, wx.ALL, 7)
        sizer_14.Add(self.label_14, 0, wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_5, 0, wx.ALL, 7)
        sizer_14.Add(self.label_15, 0, wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_4, 0, wx.ALL, 7)
        sizer_14.Add(self.label_16, 0, wx.ALL, 10)
        sizer_14.Add(self.text_ctrl_3, 0, wx.ALL, 7)
        sizer_14.Add(self.panel_4, 1, wx.EXPAND, 0)
        self.notebook_1_Proxy.SetSizer(sizer_14)
        sizer_10.Add(self.label_2, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.notebook_1_Sync.SetSizer(sizer_10)
        sizer_11.Add(self.label_3, 0, wx.ALL, 10)
        sizer_12.Add(self.checkbox_1, 0, wx.ALL, 10)
        sizer_12.Add(self.dirpickerctrl_2, 1, wx.ALL | wx.EXPAND, 0)
        sizer_11.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_11.Add(self.panel_1, 9, wx.EXPAND, 0)
        self.notebook_1_Fetch.SetSizer(sizer_11)
        sizer_13.Add(self.label_4, 0, wx.ALL, 10)
        sizer_13.Add(self.text_ctrl_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        grid_sizer_1.Add(self.label_17, 0, wx.ALL, 10)
        sizer_19.Add(self.button_2, 0, wx.ALL, 7)
        sizer_19.Add(self.label_18, 0, wx.ALL, 10)
        sizer_19.Add(self.label_19, 0, wx.ALL, 10)
        grid_sizer_1.Add(sizer_19, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_9, 0, wx.ALL, 10)
        grid_sizer_1.Add(self.hyperlink_1, 0, wx.ALL, 10)
        grid_sizer_1.Add(self.label_10, 0, wx.ALL, 10)
        grid_sizer_1.Add(self.hyperlink_2, 0, wx.ALL, 10)
        grid_sizer_1.Add(self.label_11, 0, wx.ALL, 10)
        grid_sizer_1.Add(self.hyperlink_3, 0, wx.ALL, 10)
        sizer_13.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.notebook_1_Info.SetSizer(sizer_13)
        self.notebook_1.AddPage(self.notebook_1_General, _("General"))
        self.notebook_1.AddPage(self.notebook_1_Source, _("Source"))
        self.notebook_1.AddPage(self.notebook_1_Proxy, _("Proxy"))
        self.notebook_1.AddPage(self.notebook_1_Sync, _("Synchronize / Social"))
        self.notebook_1.AddPage(self.notebook_1_Fetch, _("Manual Download"))
        self.notebook_1.AddPage(self.notebook_1_Info, _("Info"))
        sizer_1.Add(self.notebook_1, 1, wx.ALL | wx.EXPAND, 10)
        sizer_1.Add(self.button_1, 0, wx.ALIGN_RIGHT | wx.ALL, 9)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnTextTextCtrl_2(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnTextTextCtrl_2()')
        _val = self.text_ctrl_2.GetValue()
        if ':' in _val or ' ' in _val:
            logger.debug('OnTextTextCtrl_2() - No ":" in hostname')
            self.text_ctrl_2.Clear()
            self.text_ctrl_2.SetHint(_('Valid host may not include ":"'))
        else:
            self.save_settings()

    def OnTextTextCtrl_5(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnTextTextCtrl_5()')
        _val = self.text_ctrl_5.GetValue()
        if len(_val) > 0:
            try:
                _int = int(_val)
                if 0 <= _int <= 65535:
                    self.save_settings()
            except:
                logger.debug('OnTextTextCtrl_5() - No integer')
                self.text_ctrl_5.Clear()
                self.text_ctrl_5.SetHint(_('Valid port range is 0 - 65535'))
        else:
            self.text_ctrl_5.SetHint(_('Valid port range is 0 - 65535'))

    def OnTextTextCtrl_4(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnTextTextCtrl_4()')
        self.save_settings()

    def OnTextTextCtrl_3(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnTextTextCtrl_3()')
        self.save_settings()

    def OnClicked(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClicked()')
        self.save_settings()

    def OnClickedListCheckbox(self, event):
        logger.debug('OnClickedListCheckbox()')
        self.save_settings()

    def OnClickedCheckbox_7(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_7()')
        if event.GetInt():
            self.enable_Checkbox_7()
        else:
            self.disble_Checkbox_7()
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_9(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_9()')
        if event.GetInt():
            self.enable_Checkbox_9()
        else:
            self.disble_Checkbox_9()
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_2(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_10()')
        if event.GetInt():
            system_settings = self.get_proxy_system_settings()
            self.enable_proxy_settings(system_settings['address'],
                                       system_settings['port'],
                                       system_settings['username'],
                                       system_settings['password'])
        else:
            self.disable_proxy_settings()
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_10(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_10()')
        if event.GetInt():
            self.enable_Checkbox_10()
        else:
            self.disble_Checkbox_10()
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_1(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_1()')
        if event.GetInt():
            self.enable_Checkbox_1()
        else:
            self.disable_Checkbox_1()
        self.save_settings()
        event.Skip()

    def enable_Checkbox_7(self):
        logger.debug('enable_Checkbox_7()')
        self.combo_box_4.Enable()

    def disble_Checkbox_7(self):
        logger.debug('disble_Checkbox_7()')
        self.combo_box_4.Disable()

    def enable_Checkbox_9(self):
        logger.debug('enable_Checkbox_9()')
        self.combo_box_5.Enable()
        self.dirpickerctrl_1.Enable()

    def disble_Checkbox_9(self):
        logger.debug('disble_Checkbox_9()')
        self.combo_box_5.Disable()
        self.dirpickerctrl_1.Disable()

    def enable_Checkbox_10(self):
        logger.debug('enable_Checkbox_10()')
        self.combo_box_6.Enable()

    def disble_Checkbox_10(self):
        logger.debug('disble_Checkbox_10()')
        self.combo_box_6.Disable()

    def enable_Checkbox_1(self):
        logger.debug('enable_Checkbox_1()')
        self.dirpickerctrl_2.Enable()

    def disable_Checkbox_1(self):
        logger.debug('disable_Checkbox_1()')
        self.dirpickerctrl_2.Disable()

    def OnClickedCheckbox_6(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_6()')
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_8(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_8()')
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_12(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_12()')
        self.save_settings()
        event.Skip()

    def OnClickedCheckbox_11(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_11()')
        self.save_settings()
        event.Skip()

    def OnTextTextCtrl_1(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnTextTextCtrl_1()')
        event.Skip()

    def OnClickedCheckbox_3(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnClickedCheckbox_3()')
        self.save_settings()
        event.Skip()

    def OnButton_2(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnButton_2()')
        show_balloon = False
        show_version_str = True
        self.myAppUpdater = lib.wariety_app_updater.WarietyAppUpdaterThread(show_balloon, show_version_str)
        event.Skip()

    def OnButton_1(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnButton_1()')
        self.myConfig.on_close()
        self.Destroy()

    # end of class SettingsDlg

    def get_proxy_system_settings(self):
        _proxy_settings = {'address': '', 'port': '', 'username': '', 'password': ''}
        proxy_pattern = re.compile('([^:]*):?([^:@/]*)@?([^:/]*):?([^:/]*)$')
        logger.debug('get_proxy_system_settings()')
        try:
            _proxy = os.environ['HTTP_PROXY']
            result = proxy_pattern.match(_proxy)
            if result:
                if result.group(3) == '':
                    # host + port
                    _proxy_settings['address'] = str(result.group(1))
                    _proxy_settings['port'] = str(result.group(2))
                else:
                    # user + pw + host + port
                    _proxy_settings['username'] = str(result.group(1))
                    _proxy_settings['password'] = str(result.group(2))
                    _proxy_settings['address'] = str(result.group(3))
                    _proxy_settings['port'] = str(result.group(4))
        except:
            logger.debug('get_proxy_system_settings() - No system settings')
        return _proxy_settings

    def disable_proxy_settings(self):
        logger.debug('disable_Proxy_Settings()')
        self.text_ctrl_2.Disable()
        self.text_ctrl_2.ChangeValue('')
        self.text_ctrl_5.Disable()
        self.text_ctrl_5.ChangeValue('')
        self.text_ctrl_4.Disable()
        self.text_ctrl_4.ChangeValue('')
        self.text_ctrl_3.Disable()
        self.text_ctrl_3.ChangeValue('')

    def enable_proxy_settings(self, address='', port='', username='', password=''):
        logger.debug('enable_proxy_settings()')
        _system_settings = {'address': address, 'port': port, 'username': username, 'password': password}
        self.text_ctrl_2.Enable()
        self.text_ctrl_2.ChangeValue(_system_settings['address'])
        self.text_ctrl_2.SetHint(_('proxy.mydomain OR 0.0.0.0'))
        self.text_ctrl_5.Enable()
        self.text_ctrl_5.ChangeValue(_system_settings['port'])
        self.text_ctrl_5.SetHint('8080')
        self.text_ctrl_4.Enable()
        self.text_ctrl_4.ChangeValue(_system_settings['username'])
        self.text_ctrl_4.SetHint(_('Leave empty if not required...'))
        self.text_ctrl_3.Enable()
        self.text_ctrl_3.ChangeValue(_system_settings['password'])
        self.text_ctrl_3.SetHint(_('Leave empty if not required...'))

    def show_version_str(self, event, msg, update_available):
        if update_available:
            self.label_19.SetLabel("{}  ({})".format(msg, _('please get the update')))
        else:
            self.label_19.SetLabel("{}  ({})".format(msg, _('no update available')))
        self.label_19.Enable()

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        logger.debug('__init__()')
        # Content of this block not found. Did you rename this class?
        pass

    def __set_properties(self):
        logger.debug('__set_properties()')
        # Content of this block not found. Did you rename this class?
        pass

    def __do_layout(self):
        logger.debug('__do_layout()')
        # Content of this block not found. Did you rename this class?
        pass

# end of class MyFrame

class settingsDlg(wx.App):
    def OnInit(self):
        logger.debug('OnInit()')
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        self.frame.Centre()
        return True

# end of class settingsDlg


if __name__ == "__main__":
    logger.debug('Starting frame')
    app = settingsDlg(0)
    app.MainLoop()
    logger.debug('Stopping frame')
