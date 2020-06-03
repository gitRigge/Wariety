# Make windows with WX Glade
start c:\Python36\pythonw.exe c:\Users\roland\Programme\wxGlade-0.9.4\wxglade.py

python c:\Python36\Tools\scripts\2to3.py -w testing_mixin.py

python c:\temp\wxPython\demo\demo.py

# Verzeichnis für virtuelle Python Umgebungen
c:\Users\roland\.virtualenvs\

# KNOW-HOW
- SQL Statements: Do I need to escape strings?      -> No, when sticking to: c.execute(sql,(params,))
- ModuleNotFoundError: No module named 'watchdog'   -> pip install watchdog

--------------------------------

# TO-DOs
[x] Logging einbauen
[x] Logging in File und StdOut
[x] Konfiguration speichern über Neustart der Anwendung hinaus
[x] Download Quellen aktivieren und nutzen
[x] DB Maintenance
[x] Get random image
[x] Hintergrundbilder aus Manuel-DL-Ordner laden
[x] Erweitere DB Maintenance auf Fetched Folder
[x] Error messages als logging + alle IO Prozesse mit try-catch
[x] Neue Bilder werdem (in der EXE) doppelt importiert
[x] Neue Bilder nach Neustart werden gelöscht. Sollen importiert werden!
[ ] Download alle x Minuten in DL Folder
[ ] Download Quellen dynamisch einlesen
[ ] Automatisch beim Windows-Start starten
[ ] Hintergrundbild wechseln alle x Minuten
[ ] Hintergrundbild beim Start von Windows ändern
[ ] Größe des DL Folders limitieren
[ ] Taskleistensymbol animieren
[ ] Sprechblase anziegen
[ ] Versionsdatei bauen mit GIT Info
[ ] Proxy Unterstützung einbauen
[ ] Update-Check
[ ] Wallpaper teilen (WhatsApp, Twitter)
