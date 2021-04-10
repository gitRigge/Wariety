TITLE Build DEV Executable
ECHO Build DEV Executable
set PATH=c:\Python36\;c:\Python36\Lib\site-packages\;c:\Python36\Scripts\;%PATH%
set PYTHONPATH=c:\Python36\Lib\
set PYTHONHOME=c:\Python36\
git pull origin master
python fetch_release_notes.py
python make_version_file.py
pyinstaller ^
    --onefile ^
    --console ^
    --debug all ^
    --distpath .\bin ^
    --workpath .\build ^
    --version-file %cd%\VERSION ^
    --paths %cd%\wariety\ ^
    --paths %cd%\wariety_autostarter\ ^
    --paths %cd%\lib\ ^
    --paths %cd%\lib\downloaders\ ^
    --paths %cd%\data\ ^
    --log-level DEBUG ^
    --hidden-import wariety ^
    --hidden-import imghdr ^
    --hidden-import bs4 ^
    --add-data %cd%\LICENSE;.\ ^
    --add-data "%cd%\Release Notes.txt";.\ ^
    --add-data %cd%\locale\de\LC_MESSAGES\*.mo;locale\de\LC_MESSAGES\ ^
    --add-data %cd%\locale\en\LC_MESSAGES\*.mo;locale\en\LC_MESSAGES\ ^
    --add-data %cd%\wariety\*.py;wariety\ ^
    --add-data %cd%\lib\downloaders\*.py;lib\downloaders\ ^
    --add-data %cd%\data\icons\*.ico;data\icons\ ^
    --add-data %cd%\data\icons\*.png;data\icons\ ^
    --clean ^
    wariety\wariety.py
del VERSION
rmdir /S /Q build\wariety
pause