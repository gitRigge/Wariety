#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Fri Nov  8 15:37:20 2019
#

import wx
import wx.lib.mixins.listctrl as listmix
import wx.adv

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

import locale
import logging
import sys
import wariety
sys.path.insert(1, '../lib')
sys.path.insert(1, '../lib/downloaders')
import wariety_config

current_locale = locale.getdefaultlocale()[0].split("_")[0]
if getattr(sys, 'frozen', False):
    lang = gettext.translation('settingsDlg', localedir=sys._MEIPASS+'/locale', languages=[current_locale])
else:
    lang = gettext.translation('settingsDlg', localedir='locale', languages=[current_locale])
lang.install()
_ = lang.gettext

logger = logging.getLogger(__name__)

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
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.checkbox_6 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Start Wariety automatically with Windows startup\n"))
        self.checkbox_7 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Change wallpaper every"))
        self.combo_box_4 = wx.ComboBox(self.notebook_1_pane_1, wx.ID_ANY, choices=[_("2"), _("4"), _("8"), _("16"), _("32"), _("64"), _("128"), _("256")], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.checkbox_8 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Change wallpaper on Windows startup"))
        self.checkbox_9 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Download a new wallpaper image every"))
        self.combo_box_5 = wx.ComboBox(self.notebook_1_pane_1, wx.ID_ANY, choices=[_("2"), _("4"), _("8"), _("16"), _("32"), _("64"), _("128"), _("256")], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.dirpickerctrl_1 = wx.DirPickerCtrl(self.notebook_1_pane_1, wx.ID_ANY, style=wx.DIRP_DIR_MUST_EXIST | wx.DIRP_USE_TEXTCTRL | wx.DIRP_SMALL)
        self.checkbox_10 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Limit download folder size to"))
        self.combo_box_6 = wx.ComboBox(self.notebook_1_pane_1, wx.ID_ANY, choices=[_("2"), _("4"), _("8"), _("16"), _("32"), _("64"), _("128"), _("256"), _("512")], style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.checkbox_12 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Animate system tray icon on every wallpaper change"))
        self.checkbox_11 = wx.CheckBox(self.notebook_1_pane_1, wx.ID_ANY, _("Show balloon message on every wallpaper change"))
        self.panel_3 = wx.Panel(self.notebook_1_pane_1, wx.ID_ANY)
        self.notebook_1_Source = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.sources_list_ctrl_1 = SourcesListCtrl(self.notebook_1_Source, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_AUTOARRANGE)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.checkbox_1 = wx.CheckBox(self.notebook_1_pane_4, wx.ID_ANY, _("Fetch wallpapers from manual download folder"))
        self.dirpickerctrl_2 = wx.DirPickerCtrl(self.notebook_1_pane_4, wx.ID_ANY, style=wx.DIRP_DIR_MUST_EXIST | wx.DIRP_USE_TEXTCTRL | wx.DIRP_SMALL)
        self.panel_1 = wx.Panel(self.notebook_1_pane_4, wx.ID_ANY)
        self.notebook_1_Info = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.text_ctrl_1 = wx.TextCtrl(self.notebook_1_Info, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self.notebook_1_Info, wx.ID_ANY, _("https://github.com/gitRigge/wariety"), _("https://github.com/gitRigge/wariety"))
        self.hyperlink_2 = wx.adv.HyperlinkCtrl(self.notebook_1_Info, wx.ID_ANY, _("https://github.com/gitRigge/wariety/issues"), _("https://github.com/gitRigge/wariety/issues"))
        self.hyperlink_3 = wx.adv.HyperlinkCtrl(self.notebook_1_Info, wx.ID_ANY, _("https://github.com/gitRigge/wariety/pulls"), _("https://github.com/gitRigge/wariety/pulls"))
        self.panel_2 = wx.Panel(self.notebook_1_Info, wx.ID_ANY)
        self.button_1 = wx.Button(self, wx.ID_ANY, _("Close"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CHECKBOX, self.OnClicked, self.checkbox_6)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_7, self.checkbox_7)
        self.Bind(wx.EVT_COMBOBOX, self.OnClicked, self.combo_box_4)
        self.Bind(wx.EVT_CHECKBOX, self.OnClicked, self.checkbox_8)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_9, self.checkbox_9)
        self.Bind(wx.EVT_COMBOBOX, self.OnClicked, self.combo_box_5)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_10, self.checkbox_10)
        self.Bind(wx.EVT_COMBOBOX, self.OnClicked, self.combo_box_6)
        self.Bind(wx.EVT_CHECKBOX, self.OnClicked, self.checkbox_12)
        self.Bind(wx.EVT_CHECKBOX, self.OnClicked, self.checkbox_11)
        self.Bind(wx.EVT_CHECKBOX, self.OnClickedCheckbox_1, self.checkbox_1)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClose, self.button_1)
        # end wxGlade
        self.Bind(wx.EVT_CLOSE, self.OnButtonClose)
        self.sources_list_ctrl_1.EnableCheckBoxes(True)
        self.Bind(wx.EVT_LIST_ITEM_CHECKED, self.OnClickedListCheckbox, self.sources_list_ctrl_1)
        self.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.OnClickedListCheckbox, self.sources_list_ctrl_1)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnClickedListCheckbox, self.sources_list_ctrl_1)
        title = kwds.get('title', 'Wariety Settings')
        self.set_properties_received_by_main(title)
        self.myConfig = wariety_config.WarietyConfig(self.config_file)
        self.set_settings()
        ## Important: call the Centre method that centers automatically
        ## the window for you
        self.Centre()

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
        # Sources
        self.myConfig.source_windows_spotlight = self.sources_list_ctrl_1.IsItemChecked(0)
        self.myConfig.source_flickr_peter_levi = self.sources_list_ctrl_1.IsItemChecked(2)
        self.myConfig.source_bing = self.sources_list_ctrl_1.IsItemChecked(1)
        self.myConfig.source_wikimedia = self.sources_list_ctrl_1.IsItemChecked(3)
        self.myConfig.source_manual = self.checkbox_1.GetValue()

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
            self.disble_Checkbox_1()
        self.dirpickerctrl_2.SetPath(self.myConfig.manual_download_folder)
        self.checkbox_12.SetValue(self.myConfig.animate_system_tray_icon)
        self.checkbox_11.SetValue(self.myConfig.show_balloon_message)
        # Sources
        _source_windows_spotlight = self.myConfig.source_windows_spotlight
        _source_bing = self.myConfig.source_bing
        _source_flickr_peter_levi = self.myConfig.source_flickr_peter_levi
        _source_wikimedia = self.myConfig.source_wikimedia
        self.sources_list_ctrl_1.InsertColumn(0, _("Activated"), wx.LIST_FORMAT_CENTRE)
        self.sources_list_ctrl_1.InsertColumn(1, _("Type"))
        self.sources_list_ctrl_1.InsertColumn(2, _("Source"))
        sources = [
                        ['Microsoft Spotlight',r'%LOCALAPPDATA%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'],
                        ['Bing Image Of The Day','https://www.bing.com/HPImageArchive.aspx'],
                        ['Peter Levi\'s Flickr Collection','https://www.flickr.com/photos/peter-levi/'],
                        ['Wikimedia Picture Of The Day','https://commons.wikimedia.org/wiki/']
                    ]
        for item in reversed(sources):
            index = self.sources_list_ctrl_1.InsertItem(0, "")
            self.sources_list_ctrl_1.SetItem(index, 1, item[0])
            self.sources_list_ctrl_1.SetItem(index, 2, item[1])

        if _source_windows_spotlight:
            self.sources_list_ctrl_1.CheckItem(0, check=True)

        if _source_bing:
            self.sources_list_ctrl_1.CheckItem(1, check=True)

        if _source_flickr_peter_levi:
            self.sources_list_ctrl_1.CheckItem(2, check=True)

        if _source_wikimedia:
            self.sources_list_ctrl_1.CheckItem(3, check=True)

        self.sources_list_ctrl_1.SetColumnWidth(0, 70)
        self.sources_list_ctrl_1.SetColumnWidth(1, 200)
        self.sources_list_ctrl_1.SetColumnWidth(2, 480)

        self.text_ctrl_1.SetValue(self.releasenotes)

    def __set_properties(self):
        logger.debug('__set_properties()')
        # begin wxGlade: SettingsDlg.__set_properties
        self.SetTitle(_("Wariety Settings"))
        _icon = wx.NullIcon
        self.SetIcon(_icon)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.dirpickerctrl_1.SetMinSize((-1, 23))
        self.notebook_1_pane_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.notebook_1_pane_3.Enable(False)
        self.dirpickerctrl_2.SetMinSize((-1, 23))
        self.text_ctrl_1.SetMinSize((760, 100))
        self.notebook_1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DFACE))
        self.button_1.SetToolTip(_("Hit button to save and close"))
        self.button_1.SetFocus()
        # end wxGlade
        if getattr(sys, 'frozen', False):
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap(sys._MEIPASS+'/data/logo_1_32x32px.ico', wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
        else:
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap('data/logo_1_32x32px.ico', wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)

    def __do_layout(self):
        logger.debug('__do_layout()')
        # begin wxGlade: SettingsDlg.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        label_5 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("General"))
        label_5.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_3.Add(label_5, 0, wx.ALL, 10)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_4.Add(self.checkbox_6, 0, wx.ALL, 10)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_5.Add(self.checkbox_7, 0, wx.ALL, 10)
        sizer_5.Add(self.combo_box_4, 0, wx.ALL, 6)
        label_6 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("Minutes"))
        sizer_5.Add(label_6, 0, wx.ALL, 10)
        sizer_2.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.checkbox_8, 0, wx.ALL, 10)
        sizer_2.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_7.Add(self.checkbox_9, 0, wx.ALL, 10)
        sizer_7.Add(self.combo_box_5, 0, wx.ALL, 6)
        label_7 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("Minutes into the folder"))
        sizer_7.Add(label_7, 0, wx.ALL, 10)
        sizer_7.Add(self.dirpickerctrl_1, 1, wx.ALL | wx.EXPAND, 0)
        sizer_2.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_8.Add(self.checkbox_10, 0, wx.ALL, 10)
        sizer_8.Add(self.combo_box_6, 0, wx.ALL, 6)
        label_8 = wx.StaticText(self.notebook_1_pane_1, wx.ID_ANY, _("MB (older files are deleted if necessary)"))
        sizer_8.Add(label_8, 0, wx.ALL, 10)
        sizer_2.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_2.Add(self.checkbox_12, 0, wx.ALL, 10)
        sizer_2.Add(self.checkbox_11, 0, wx.ALL, 10)
        sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_2)
        label_1 = wx.StaticText(self.notebook_1_Source, wx.ID_ANY, _("Image Sources"))
        label_1.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.sizer_9.Add(label_1, 0, wx.ALL, 10)
        self.sizer_9.Add(self.sources_list_ctrl_1, 1, wx.EXPAND, 0)
        self.notebook_1_Source.SetSizer(self.sizer_9)
        label_2 = wx.StaticText(self.notebook_1_pane_3, wx.ID_ANY, _("VRTY.ORG is currently not publically available"))
        sizer_10.Add(label_2, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.notebook_1_pane_3.SetSizer(sizer_10)
        label_3 = wx.StaticText(self.notebook_1_pane_4, wx.ID_ANY, _("Fetch folder"))
        label_3.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_11.Add(label_3, 0, wx.ALL, 10)
        sizer_12.Add(self.checkbox_1, 0, wx.ALL, 10)
        sizer_12.Add(self.dirpickerctrl_2, 1, wx.ALL | wx.EXPAND, 0)
        sizer_11.Add(sizer_12, 1, wx.EXPAND, 0)
        sizer_11.Add(self.panel_1, 9, wx.EXPAND, 0)
        self.notebook_1_pane_4.SetSizer(sizer_11)
        label_4 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Recent changes"))
        label_4.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_13.Add(label_4, 0, wx.ALL, 10)
        sizer_13.Add(self.text_ctrl_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        label_9 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Visit project page"))
        label_9.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_13.Add(label_9, 0, wx.ALL, 10)
        sizer_13.Add(self.hyperlink_1, 0, wx.ALL, 10)
        label_10 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Bug report / issue tracker"))
        label_10.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_13.Add(label_10, 0, wx.ALL, 10)
        sizer_13.Add(self.hyperlink_2, 0, wx.ALL, 10)
        label_11 = wx.StaticText(self.notebook_1_Info, wx.ID_ANY, _("Change requests"))
        label_11.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_13.Add(label_11, 0, wx.ALL, 10)
        sizer_13.Add(self.hyperlink_3, 0, wx.ALL, 10)
        sizer_13.Add(self.panel_2, 1, wx.EXPAND, 0)
        self.notebook_1_Info.SetSizer(sizer_13)
        self.notebook_1.AddPage(self.notebook_1_pane_1, _("General"))
        self.notebook_1.AddPage(self.notebook_1_Source, _("Source"))
        self.notebook_1.AddPage(self.notebook_1_pane_3, _("Synchronize / Social"))
        self.notebook_1.AddPage(self.notebook_1_pane_4, _("Manual Download"))
        self.notebook_1.AddPage(self.notebook_1_Info, _("Info"))
        sizer_1.Add(self.notebook_1, 1, wx.ALL | wx.EXPAND, 10)
        sizer_1.Add(self.button_1, 0, wx.ALIGN_RIGHT | wx.ALL, 9)
        self.SetSizer(sizer_1)
        self.Layout()
        self.Centre()
        # end wxGlade

    def OnButtonClose(self, event):  # wxGlade: SettingsDlg.<event_handler>
        logger.debug('OnButtonClose()')
        self.myConfig.on_close()
        self.Destroy()

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
            self.disble_Checkbox_1()
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

    def disble_Checkbox_1(self):
        logger.debug('disble_Checkbox_1()')
        self.dirpickerctrl_2.Disable()

# end of class SettingsDlg

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

    def OnButtonClose(self, event):  # wxGlade: MyFrame.<event_handler>
        logger.debug('OnButtonClose()')
        print("Event handler 'OnButtonClose' not implemented!")
        event.Skip()

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