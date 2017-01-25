#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
NEW_FILENAME = os.path.join(BASE_DIR,'view')
NAME_PWD = os.path.join(BASE_DIR,'config','db')
USER_FILE = os.path.join(BASE_DIR,'config')


import os
DIR_BASES=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BIND_HOST='127.0.0.1'
BIND_PORT=9997

USER_BASE_HOME_PATH='%s/var/users'%BASE_DIR