TITLE Build PROD Executable
ECHO Build PROD Executable
set PATH=c:\Python36\;c:\Python36\Lib\site-packages\;c:\Python36\Scripts\;%PATH%
set PYTHONPATH=c:\Python36\Lib\
set PYTHONHOME=c:\Python36\
git stash
git pull origin master
python make_version_file.py
REM Error code 0 == Non Dev status
if %ERRORLEVEL%==0 (
python fetch_release_notes.py
pyinstaller ^
        --onefile ^
        --noconsole ^
        --distpath .\bin ^
        --workpath .\build ^
        --version-file %cd%\VERSION ^
        --paths %cd%\wariety\ ^
        --paths %cd%\lib\ ^
        --paths %cd%\lib\downloaders\ ^
        --paths %cd%\data\ ^
        --clean ^
        --log-level INFO ^
        --hidden-import wariety ^
        --hidden-import imghdr ^
        --hidden-import bs4 ^
        --hidden-import datetime ^
        --name Wariety ^
        --add-data %cd%\LICENSE;.\ ^
        --add-data "%cd%\Release Notes.txt";.\ ^
        --add-data %cd%\locale\de\LC_MESSAGES\*.mo;locale\de\LC_MESSAGES\ ^
        --add-data %cd%\locale\en\LC_MESSAGES\*.mo;locale\en\LC_MESSAGES\ ^
        --add-data %cd%\wariety\*.py;wariety\ ^
        --add-data %cd%\lib\downloaders\*.py;lib\downloaders\ ^
        --add-data %cd%\data\icons\*.ico;data\icons\ ^
        --add-data %cd%\data\icons\*.png;data\icons\ ^
        --icon %cd%\data\icons\logo_1_32x32px.ico ^
        --clean ^
    wariety\wariety.py
rmdir /S /Q build\wariety
) else (
    echo.
    echo Development status found - no PROD build
)
@echo off
del VERSION
del Release Notes.txt
git stash pop
pause