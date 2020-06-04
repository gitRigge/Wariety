#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from subprocess import check_output
print('FETCH RELEASE NOTES: Read properties')
release_notes = check_output('git log --all --grep="#releasenotes" --pretty=format:"%s (%h)"', shell=True).decode()
release_notes = release_notes.replace(' #releasenotes','')

print('FETCH RELEASE NOTES: Write release notes')
f = open('Release Notes.txt', 'w')
f.write(release_notes)
f.close()

print('FETCH RELEASE NOTES: Successfully finished')
sys.exit()