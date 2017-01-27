#!/usr/bin/env python
# -*- coding=utf8 -*-

import os,sys
import socket
import json
import time
from decimal import getcontext, Decimal
from passwd import getpass
import tab

class FTPClient(object):
    response_code={
            '200':' user passed authentication!',
            '201':'Invalid use or password',
            '202':'user expired',
            '300':'ready to send',
            '301':'ready to recv',
            '100':'finish',
        }
    getcontext().prec = 2
    def __init__(self,argv):
        self.args=argv

        print(self.args)
        self.parser_argv()
        self.connect()
        self.handle()

    def parser_argv(self):
        if len(self.args)<5:
            print('ok')
            self.help_msg()
        else:
            mandatory_field=['-s','-p']
            for i in mandatory_field:
                if i not in sys.argv:
                    sys.exit('the argument [%s] is mandatory!'%i)
            try:

                self.ftp_host=self.args[self.args.index('-s')+1]
                self.ftp_port=int(self.args[self.args.index('-p')+1])
            except (IndexError,ValueError) as e:
                print(e)
                self.help_msg()

            print(self.ftp_port,self.ftp_host)

    def connect(self):
        try:
            self.sock=socket.socket()
            self.sock.connect((self.ftp_host,self.ftp_port))
            #self.sock.timeout(5)
        except socket.error as e :
            sys.exit(e)

    def handle(self):
        if self.auth():
            self.interactive()

    def auth(self):
        count=0
        while count<3:

            username=raw_input('username:').strip()
            if len(username)==0:continue
            # password=raw_input('password:').strip()
            print "password:",
            password = getpass("*").strip()
            if len(password)==0:continue
            data=json.dumps({'username':username,
                             'password':password,
                             'action':'user_auth',
                             })
            self.sock.sendall(data)
            server_response=json.loads(self.sock.recv(1024))
            if server_response['status']=='200':
                print(self.response_code['200'])
                self.user=username
                self.cwd='/'
                return True
            else:
                print(self.response_code[server_response['status']])
                count+=1
        else:
            self.cmd_quit("quit")
            # sys.exit('Too many attempt!')

    def interactive(self):
        quit_flag=False
        while  not quit_flag:
            user_input=raw_input('[%s][%s] '%(self.user,self.cwd)).strip()
            if len(user_input)==0:
                continue
            self.cmd_parser(user_input)

    def cmd_parser(self,user_input):
        cmd_list=user_input.split()
        if hasattr(self,'cmd_'+cmd_list[0]):
            func=getattr(self,'cmd_'+cmd_list[0])
            func(cmd_list)
        else:
            print 'INVALID CMD'

    def cmd_get(self,cmd_list):
        if len(cmd_list)<2:
            print (' filename is mandatory!')
        else:
            remote_filename=cmd_list[1]
            msg_str={'action':'cmd_get',
                     'filename':remote_filename
                     }
            self.sock.send(json.dumps(msg_str))
            server_response=json.loads(self.sock.recv(1024))
            print server_response
            #server_response={'status':300,'data':[{'filename':'xxx','size':333},]}
            if server_response.get('status')=='300':
                # local_filename=os.path.basename(remote_filename)
                local_filename = "%s/%s"%(os.path.dirname(__file__),remote_filename.split("/")[-1])
                print(local_filename)
                if os.path.exists("%s/%s"%(os.path.dirname(__file__),remote_filename.split("/")[-1])):
                    os.system("sed -i '$d' %s"%local_filename)
                    received_size=local_size = os.stat("%s/%s"%(os.path.dirname(__file__),remote_filename.split("/")[-1])).st_size
                else:
                    received_size=local_size=0
                total_file_size=int(server_response['data'][0].get('size'))
                client_response={'action':'cd_get',
                                 'status':'301',
                                 'data':[{'filename':remote_filename,'has_send':local_size}]
                                 }
                print(local_size)
                self.sock.send(json.dumps(client_response))
                if received_size:
                    file_action = "ab"
                else:
                    file_action = "wb"
                f=open(local_filename,'%s'%file_action)
                while int(total_file_size) != int(received_size):
                    data=self.sock.recv(4096)

                    received_size+=len(data)

                    f.write(data)
                    sys.stdout.write('\r')
                    num1 = int(Decimal(received_size)/total_file_size*100)
                    num2 = int(Decimal(received_size)/total_file_size*50)*'='
                    time.sleep(0.1)
                    sys.stdout.write('已发送%s%%|%s' %(num1,num2))
                    sys.stdout.flush()
                else:
                    print (' %s 下载成功！\n'%remote_filename.split("/")[-1])
            else:print('%s 不是文件！'%remote_filename)

    def cmd_put(self,cmd_list):
        print("cmd_list-->%s"%cmd_list)
        if len(cmd_list)<2:
            print (' filename is mandatory!')
        else:
            filename=cmd_list[1]
            if os.path.isfile(filename):
                if os.path.exists(filename):
                    size = os.stat(filename).st_size
                    msg_str={'action':'cmd_put',
                             'filename':filename.split('/')[-1],
                             'size':size
                             }
                    self.sock.send(json.dumps(msg_str))
                    server_response=json.loads(self.sock.recv(1024))
                    print server_response
                    #server_response={'status':300,'data':[{'filename':'xxx','size':333},]}
                    if server_response.get('status')=='300':
                            if server_response['data'][0].get('has_send'):
                                has_send = int(server_response['data'][0].get('has_send'))
                            else:
                                has_send = 0
                            print('has_send:%s'%has_send)
                            with open(filename,'rb') as files:
                                files.seek(has_send,0)
                                while has_send < size:
                                    data = files.read(4096)
                                    self.sock.send(data)
                                    has_send += len(data)
                                    sys.stdout.write('\r')
                                    num1 = int(Decimal(has_send)/size*100)
                                    num2 = int(Decimal(has_send)/size*50)*'='
                                    time.sleep(0.1)
                                    sys.stdout.write('已发送%s%%|%s' %(num1,num2))
                                    sys.stdout.flush()
                            print(" %s 上传成功\n"%filename)
                            client_response={'action':'put',
                                    'status':'100'
                                    }
                            self.sock.send(json.dumps(client_response))
                else:
                    print("%s 不存在！"%filename)
            else:
                print("%s 不是文件！"%filename)
    def cmd_ls(self,cmd_list=""):
        msg_str={'action':'cmd_ls',
                 'path':cmd_list
                     }
        self.sock.send(json.dumps(msg_str))
        data=self.sock.recv(4096)
        print(data)
        '''
        # 在这里是实现ls功能，并每行显示4个
        tmp_list=[]
        # counter = 1
        # data_len = len(data.split("\n"))
        # num = (data_num/4)*4
        for i in data.split("\n"):
            if len(tmp_list) == 4:
                print("%s   %s   %s   %s"%(tmp_list[0],tmp_list[1],tmp_list[2],tmp_list[3]))
                tmp_list=[]
            else:
                tmp_list.append(i)
                # counter += 1
        # if counter == data_len:
        if len(tmp_list) == 3:
            print("%s   %s   %s\n"%(tmp_list[0],tmp_list[1],tmp_list[2]))
        elif len(tmp_list) == 2:
            print("%s   %s\n"%(tmp_list[0],tmp_list[1]))
        else:
            print("%s\n"%tmp_list[0])
        '''

    def cmd_pwd(self,cmd_list):
        msg_str={'action':'cmd_pwd',
                     }
        self.sock.send(json.dumps(msg_str))
        data=self.sock.recv(4096)
        print(data)

    def cmd_cd(self,cmd_list):
        msg_str={'action':'cmd_cd',
                  'path':cmd_list
                     }
        self.sock.send(json.dumps(msg_str))
        # data=self.sock.recv(4096)
        # print(data)


    def cmd_quit(self,cmd_list):
        msg_str={'action':'cmd_quit',
                     }
        self.sock.send(json.dumps(msg_str))
        time.sleep(1)
        self.sock.close()
        sys.exit('quit!')

    def help_msg(self):

        help_msg='''
        -s ftp_addr     :the ftp server you want connect mandatory

        -p ftp port     :ftp port mandatory
        '''
        sys.exit(help_msg)
