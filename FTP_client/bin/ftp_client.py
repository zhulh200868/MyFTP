#!/usr/bin/env python
# -*- coding=utf8 -*-

import sys ,os

DIR_BASES=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASES)
from core  import socket_client


if __name__=='__main__':
    FtpClient=socket_client.FTPClient (sys.argv)
