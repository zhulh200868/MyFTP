#!/usr/bin/env python
# -*- coding=utf8 -*-

import SocketServer
import json
import sys,os
DIR_BASES=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASES)
import auth
from logger import logger
from config import settings
import commands

class FtpServer(SocketServer.BaseRequestHandler):
    response_code={
            '200':' user passed authentication!',
            '201':'Invalid use or password',
            '202':'user expired',
            '300':'ready to send',
            '301':'ready to recv'}

    def handle(self):
        logger.info(' - %s'%str(self.client_address))
        # print (self.client_address)
        self.shutdown_flag=True
        while self.shutdown_flag:
            data=self.request.recv(1024)
            self.data_parser(data)

    def data_parser(self,data):
        try:
            data=json.loads(data)
            # print(data)
            logger.info(" - %s"%str(data))
            if data.get('action'):
                  action_type=data['action']
                  if hasattr(self,action_type):
                      func=getattr(self,action_type)
                      func(data)
                  else:
                      logger.warning(" - invalid action type !")
                      # print('invalid action type ')

            else:
                logger.warning(" - invalid")
                # print('invalid')
        except Exception,e:
            logger.warning(" - %s"%str(e))

    def cmd_get(self,data):
        # print (' - client ask for downloading data',str(data))
        logger.info(" - client ask for downloading data,%s"%str(data))
        if hasattr(self,'login_user'):
            filename_path=data.get('filename')
            file_abs_path='%s/%s'%(self.home_path,filename_path)

            if os.path.isfile(file_abs_path):
                file_size=os.path.getsize(file_abs_path)
                response_data={'status':'300',
                               'data':[{'filename':filename_path,'size':file_size}]}
                self.request.send(json.dumps(response_data))
                client_response=json.loads(self.request.recv(1024))
                # print(client_response)
                logger.info(" - %s"%str(client_response))
                if client_response.get('status')=='301':
                    f=open(file_abs_path,'rb')
                    has_send = client_response['data'][0].get('has_send')
                    f.seek(has_send,0)
                    # print has_send,file_size
                    while  int(file_size) != int(has_send):
                        data=f.read(4096)
                        self.request.send(data)
                        has_send+=len(data)
                        # print has_send,file_size
                    else:
                        # print 'send file done'
                        logger.info(' - send file done !')
                        f.close()
            else:
                response_data={'status':'401',
                        'data':[{'filename':filename_path,'size':0}]}
                self.request.send(json.dumps(response_data))
            #print ('the file dose not exist!')

        #print 'user is not authorized!'

    def cmd_put(self,data):
        # print ('client ask for loading data',data)
        logger.info(" - client ask for loading data,%s"%str(data))
        if hasattr(self,'login_user'):
            filename_path=data.get('filename')
            file_abs_path='%s/%s'%(self.home_path,filename_path)
            file_size = data.get('size')
            if os.path.exists(file_abs_path):
                os.system("sed -i '$d' %s"%file_abs_path)
                local_size = os.stat(file_abs_path).st_size
                response_data={'status':'300',
                    'data':[{'filename':file_abs_path,'has_send':local_size}]}
                file_action = "ab"
                has_recv = int(local_size)
                # if has_recv < int(file_size):
                #     os.system("sed -i '$d' %s"%file_abs_path)
            else:
                response_data={'status':'300',
                    'data':[{'filename':file_abs_path,'has_send':0}]}
                has_recv = 0
                file_action = "wb"
            self.request.send(json.dumps(response_data))
            with open(file_abs_path,'%s'%file_action) as files:
                while has_recv <= int(file_size):
                    data = self.request.recv(4096)
                    #判断是否结束
                    try:
                        if json.loads(data)['action'] == 'put' and json.loads(data)['status'] == '100':
                            logger.info(' - load file done !')
                            break
                    except Exception,e:
                        files.write(data)
                        has_recv += len(data)
            # else:
            #     response_data={'status':'401',
            #             'data':[{'filename':file_abs_path,'has_send':0}]}
            #     self.request.send(json.dumps(response_data))

    def cmd_ls(self,data):
        # self.request.send("hello")
        # logger.debug(data.get('path'))
        if len(data.get('path')) == 2:
            status,output = commands.getstatusoutput("%s -l %s"%(data.get('path')[0],data.get('path')[1]))
        else:
            status,output = commands.getstatusoutput("ls -l %s"%self.current_path)
        '''
        # 这里实现是ls的功能
        if len(data.get('path')) == 2:
            status,output = commands.getstatusoutput("%s %s"%(data.get('path')[0],data.get('path')[1]))
        else:
            status,output = commands.getstatusoutput("ls %s"%self.current_path)
        '''
        # logger.debug(" - %s"%str(output))
        if status:
            pass
        else:
            self.request.send(output)

    def cmd_pwd(self,data):
        self.request.send(self.current_path)

    def cmd_cd(self,data):
        if len(data.get('path')) == 2:
            self.current_path = data.get('path')[1]
        else:
            self.current_path = self.home_path


    def cmd_quit(self,data):
        self.shutdown_flag = False
        logger.info(" - %s is quited !"%str(self.client_address))

    def user_auth(self,data):
        username=data.get('username')
        password=data.get('password')

        auth_status,auth_msg=auth.authentication(username,password)
        # print (auth_msg,auth_status)
        # auth_status = True
        if auth_status:
            # print('authentication',auth_msg)
            logger.info(" - authentication,%s"%auth_msg)
            response_data={'status':'200','data':[]}
            self.login_user=username
            self.home_path='%s/%s'%(settings.USER_BASE_HOME_PATH,username)
            if os.path.exists(self.home_path) is False:
                os.mkdir(self.home_path)
            self.current_path=self.home_path

        else:
            # print('authentication failed',auth_msg)
            logger.warning(" - authentication failed,%s"%auth_msg)
            response_data={'status':'201','data':[]}
        self.request.send(json.dumps(response_data))









