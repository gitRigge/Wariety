import logging
import os
import sys
logger = logging.getLogger(__name__)
logger.debug('data\\downloaders\\__init__().py')
CWD = os.path.dirname(os.path.realpath(__file__))
print(CWD)
-mod_path1 = os.path.abspath(os.path.join(CWD, '../lib'))
-mod_path2 = os.path.abspath(os.path.join(CWD, '../lib/downloaders'))
-mod_path3 = os.path.abspath(os.path.join(CWD, '../wariety'))
sys.path.insert(1, -mod_path1)
sys.path.insert(1, -mod_path2)
sys.path.insert(1, -mod_path3)
