TITLE Build DEV Executable
ECHO Build DEV Executable
set PATH=c:\Python36\;c:\Python36\Lib\site-packages\;c:\Python36\Scripts\;%PATH%
set PYTHONPATH=c:\Python36\Lib\
set PYTHONHOME=c:\Python36\

python make_version_file.py
REM Error code 1 == Dev status
if %ERRORLEVEL%==1 (
python fetch_release_notes.py
pyinstaller ^
    --onefile ^
    --console ^
    --debug all ^
    --distpath .\bin ^
    --workpath .\build ^
    --version-file %cd%\VERSION ^
    --paths %cd%\wariety\ ^
    --paths %cd%\lib\ ^
    --paths %cd%\lib\downloaders\ ^
    --paths %cd%\data\ ^
    --log-level DEBUG ^
    --hidden-import wariety ^
    --hidden-import imghdr ^
    --hidden-import bs4 ^
    --hidden-import datetime ^
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
rmdir /S /Q build\wariety
) else (
    echo.
    echo Non-Development status found - no DEV build
)
@echo off
del VERSION
del /F "Release Notes.txt"
pause