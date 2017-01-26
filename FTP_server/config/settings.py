#!/usr/bin/env python
# -*- coding=utf8 -*-

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BIND_HOST='127.0.0.1'
BIND_PORT=9997

USER_BASE_HOME_PATH='%s/var/users'%BASE_DIR

log_level="debug"

log_file="ftp.log"

ACCOUNT_DB={
    "engine":"file",
    "name":"%s/config/db"%BASE_DIR
}