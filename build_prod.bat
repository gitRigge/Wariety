TITLE Build PROD Executable
ECHO Build PROD Executable
set PATH=c:\Python36\;c:\Python36\Lib\site-packages\;c:\Python36\Scripts\;%PATH%
set PYTHONPATH=c:\Python36\Lib\
set PYTHONHOME=c:\Python36\
pyinstaller ^
    --onefile ^
    --noconsole ^
    --distpath bin ^
    --paths c:\Users\roland\Programming\Privat\wariety.git\wariety ^
    --paths c:\Users\roland\Programming\Privat\wariety.git\lib ^
    --paths c:\Users\roland\Programming\Privat\wariety.git\lib\downloaders\ ^
    --clean ^
    --log-level INFO ^
    --hidden-import wariety ^
    --name Wariety ^
    --version-file c:\Users\roland\Programming\Privat\wariety.git\VERSION ^
    --icon c:\Users\roland\Programming\Privat\wariety.git\data\logo_1_32x32px.ico ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\locale\de\LC_MESSAGES\*.mo;locale\de\LC_MESSAGES\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\locale\en\LC_MESSAGES\*.mo;locale\en\LC_MESSAGES\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\data\*.ico;data\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\data\*.png;data\ ^
    wariety\wariety.py
pause