TITLE Make POT Files
ECHO Make POT Files
set PATH=c:\Python36\;c:\Python36\Lib\site-packages\;c:\Python36\Scripts\;%PATH%
set PYTHONPATH=c:\Python36\Lib\
set PYTHONHOME=c:\Python36\
python c:\Python36\Tools\i18n\pygettext.py --verbose --output=c:\Users\roland\\Programming\Privat\wariety.git\locale\wariety.pot wariety\wariety.py
python c:\Python36\Tools\i18n\pygettext.py --verbose --output=c:\Users\roland\\Programming\Privat\wariety.git\locale\aboutDlg.pot wariety\aboutDlg.py
python c:\Python36\Tools\i18n\pygettext.py --verbose --output=c:\Users\roland\\Programming\Privat\wariety.git\locale\settingsDlg.pot wariety\settingsDlg.py
pause