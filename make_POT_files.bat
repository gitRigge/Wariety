TITLE Make POT Files
@echo off
ECHO Make POT Files
set PATH=c:\Python312\;c:\Python312\Lib\site-packages\;c:\Python312\Scripts\;%PATH%
set PYTHONPATH=c:\Python312\Lib\
set PYTHONHOME=c:\Python312\
python c:\Python36\Tools\i18n\pygettext.py --verbose --output=%cd%\locale\wariety.pot wariety\wariety.py
python c:\Python36\Tools\i18n\pygettext.py --verbose --output=%cd%\locale\aboutDlg.pot wariety\aboutDlg.py
python c:\Python36\Tools\i18n\pygettext.py --verbose --output=%cd%\locale\settingsDlg.pot wariety\settingsDlg.py
pause