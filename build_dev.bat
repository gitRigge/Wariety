TITLE Build DEV Executable
ECHO Build DEV Executable
set PATH=c:\Python36\;c:\Python36\Lib\site-packages\;c:\Python36\Scripts\;%PATH%
set PYTHONPATH=c:\Python36\Lib\
set PYTHONHOME=c:\Python36\
pyinstaller ^
    --onefile ^
    --console ^
    --debug all ^
    --distpath bin ^
    --version-file c:\Users\roland\Programming\Privat\wariety.git\VERSION ^
    --paths c:\Users\roland\Programming\Privat\wariety.git\wariety\ ^
    --paths c:\Users\roland\Programming\Privat\wariety.git\lib\ ^
    --paths c:\Users\roland\Programming\Privat\wariety.git\lib\downloaders\ ^
    --log-level DEBUG ^
    --hidden-import wariety ^
    --hidden-import imghdr ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\LICENSE;.\ ^
    --add-data "c:\Users\roland\Programming\Privat\wariety.git\Release Notes.txt";.\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\locale\de\LC_MESSAGES\*.mo;locale\de\LC_MESSAGES\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\locale\en\LC_MESSAGES\*.mo;locale\en\LC_MESSAGES\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\data\*.ico;data\ ^
    --add-data c:\Users\roland\Programming\Privat\wariety.git\data\*.png;data\ ^
    --clean ^
    wariety\wariety.py
pause