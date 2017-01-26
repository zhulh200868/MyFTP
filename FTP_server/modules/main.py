#!/usr/bin/env python
# -*- coding=utf8 -*-


import sys,os
DIR_BASES=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASES)
from modules import socket_server
from config import settings
import commands,signal
from logger import logger
import pickle

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
        logger.info("Ftp_server is starting !")
        server.serve_forever()

    def stop(self):
        with open('/var/run/ftp.pid') as ftp:
            for line in ftp:
                pid = line
        try:
            os.kill(int(pid.strip()), signal.SIGKILL)
            logger.info("Ftp_server is stopping !")
        except OSError, e:
            print '没有如此进程!!!'

    def create(self):
        username = raw_input("username: ")
        passwd = raw_input("password: ")
        data = {username:passwd}
        if os.path.exists("%s"%settings.ACCOUNT_DB.get('name')):
            value=pickle.load(open(settings.ACCOUNT_DB.get('name'),'rb'))
            dictMerged1=dict(data.items()+value.items())
            data = dictMerged1.copy()
        pickle.dump(data,open(settings.ACCOUNT_DB.get('name'),'wb'))



    def help_msg(self):
        msg='''
                start          :satrt ftp server
                stop           :stop ftp server
                create         :create ftp user account
                help           :print help_msg

            '''
        sys.exit(msg)