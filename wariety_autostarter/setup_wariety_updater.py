#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Wariety - A wallpaper manager for MS Windows operating system.
# Copyright (C) 2020  Roland Rickborn <wariety@gmx.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

CONTENT = """@echo off

setlocal enabledelayedexpansion

set folder1=AAA
set folder2=BBB

set count=0
set x=0

REM put all the files into a pseudo-array prefixed with "PIC_"
for /r "%folder1%" %%a in (*.*) do (
    set PIC_!count!=%%~a
    set /a count+=1
)

for /r "%folder2%" %%a in (*.*) do (
    set PIC_!count!=%%~a
    set /a count+=1
)

REM Use the 'modulo' function to get a usable value from system variable %random%
set /a x="%random% %% count"

REM Pull the relevant item out of the "PIC_" 'array'
set chosen=!PIC_%x%!

echo:I chose :: %chosen%
reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "%chosen%" /f
RUNDLL32.EXE USER32.DLL, UpdatePerUserSystemParameters
ping 127.0.0.1 -n 1 > nul
"""


def write_batch_file(filenamepath, download_folder, fetch_folder):
    _file_content = CONTENT.replace('AAA', download_folder).replace('BBB', fetch_folder)
    f = open(filenamepath, 'w')
    f.write(_file_content)
    f.close()
