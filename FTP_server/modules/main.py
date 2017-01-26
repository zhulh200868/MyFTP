#!/usr/bin/env python
# -*- coding=utf8 -*-


import sys,os
DIR_BASES=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASES)
from modules import socket_server
from config import settings
import commands,signal
from logger import logger
from multiprocessing import Pool,Process

class FtpHander(object):
    def __init__(self,args):
        self.args=args
        #print(self.args)
        self.ftp_parser()
    def ftp_parser(self):
        if len(self.args)==1:
            self.help_msg()
        else:
            if hasattr(self,self.args[1]):
                func=getattr(self,self.args[1])
                func()
            else:
                self.help_msg()
    def start(self) :
        server=socket_server.SocketServer.ThreadingTCPServer((settings.BIND_HOST,settings.BIND_PORT),socket_server.FtpServer)
        server.serve_forever()

    def stop(self):
        with open('/var/run/ftp.pid') as ftp:
            for line in ftp:
                pid = line
        try:
            os.kill(int(pid.strip()), signal.SIGKILL)
            logger.info("Ftp_server is stopped !")
        except OSError, e:
            print '没有如此进程!!!'



    def help_msg(self):
        msg='''
                start          :satrt ftp server
                stop           :stop ftp server
                create         :create ftp user account
                help           :print help_msg

            '''
        sys.exit(msg)