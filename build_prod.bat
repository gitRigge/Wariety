TITLE Build PROD Executable
@echo off
ECHO Build PROD Executable
echo.
set PATH=c:\Python312\;c:\Python312\Lib\site-packages\;c:\Python312\Scripts\;%PATH%
set PYTHONPATH=c:\Python312\Lib\
set PYTHONHOME=c:\Python312\
git stash
git pull origin master
python make_version_file.py
echo.
REM Error code 0 == Non Dev status
if %ERRORLEVEL%==0 (
    python fetch_release_notes.py
    echo.
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
del VERSION
git rm -f -q "Release Notes.txt"
del /F "Release Notes.txt"
git stash pop
pause