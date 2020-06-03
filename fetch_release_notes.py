#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from subprocess import check_output
release_notes = check_output('git log --all --grep="#releasenotes" --pretty=format:"%s (%h)"', shell=True).decode()
release_notes = release_notes.replace(' #releasenotes','')

f = open('Release Notes.txt', 'w')
f.write(release_notes)
f.close()

sys.exit()