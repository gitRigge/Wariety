#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
sys.path.insert(1, 'lib')
import wariety.wariety
from subprocess import check_output

def get_version_array(vers_str):
    vers_arr = vers_str.split('.')
    l = len(vers_arr)
    d = 4 - l
    for i in range(0, d):
        vers_arr.insert(0, i)
    return vers_arr

print('MAKE VERSION FILE: Read properties')
cmt_msg = check_output('git log --all --grep="#releasenotes" --pretty=format:"%h" --max-count 1', shell=True).decode()
branch = check_output('git branch --format %(refname:short)', shell=True).decode()
version_str = wariety.wariety.__version__
version_arr = get_version_array(version_str)
author = wariety.wariety.__author__
appname = wariety.wariety.APP_NAME
copyright = wariety.wariety.__copyright__


version_info_dic = {
    'R01': version_arr[0], # Version x.0.0.0
    'R02': version_arr[1], # Version 0.x.0.0
    'R03': version_arr[2], # Version 0.0.x.0
    'R04': version_arr[3], # Version 0.0.0.x
    'R05': author,  # CompanyName -> author
    'R06': 'Wallpaper manager for Windows',  # FileDescription
    'R07': version_str,  # FileVersion -> version
    'R08': appname,  # InternalName -> APP_NAME
    'R09': copyright,  # LegalCopyright -> copyright
    'R10': 'wariety.exe',  # OriginalFilename
    'R11': appname,  # ProductName -> APP_NAME
    'R12': '{} ({} {})'.format(version_str, branch.split('\n')[0].strip(), cmt_msg)   # ProductVersion -> version + (cmt_msg)
}

print('MAKE VERSION FILE: Read template')
f = open(r'VERSION.bak', 'r')
template = f.read()
f.close()

for item in version_info_dic:
    template = template.replace(item, str(version_info_dic[item]))

print('MAKE VERSION FILE: Write version file')
f = open('VERSION', 'w')
f.write(template)
f.close()

print('MAKE VERSION FILE: Successfully finished')
sys.exit()