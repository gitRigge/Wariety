#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Wariety - A wallpaper manager for MS Windows operating system.
# Copyright (C) 2024  Roland Rickborn <wariety@gmx.net>
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

import sys
from subprocess import check_output
print('FETCH RELEASE NOTES: Read properties')
tmp_notes = check_output('git log --all --grep="#releasenotes" --pretty=format:"%s (%h)"', shell=True).decode().split('\n')
lines = []
release_notes = ''
for line in tmp_notes:
    if line[0].isdigit():
        lines.append(line)
release_notes = '\n'.join(lines)
release_notes = release_notes.replace(' #releasenotes', '')

print('FETCH RELEASE NOTES: Write release notes')
f = open('Release Notes.txt', 'w')
f.write(release_notes)
f.close()

print('FETCH RELEASE NOTES: Successfully finished')
sys.exit()