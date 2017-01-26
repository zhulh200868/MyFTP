#!/usr/bin/env python
# -*- coding=utf8 -*-

import os,sys
DIR_BASES=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIR_BASES)
from config import settings
import json,pickle

def fetch_account():
    acc_storage=settings.ACCOUNT_DB.get('engine')
    if hasattr(sys.modules[__name__],'engine_'+acc_storage):
        obj=getattr(sys.modules[__name__],'engine_'+acc_storage)
        return obj()



class engine_file():
    def auth(self,username,password):
        file_name=settings.ACCOUNT_DB.get('name')
        # assert file_name is not None
        # # f=open(file_name,'rb')
        # acc_dic=json.load(f)
        value = pickle.load(open(settings.ACCOUNT_DB.get('name'),'rb'))
        if username in value.keys():
            if password == value.get(username):
                msg=('pass authentication')
                status=True
                return status,msg
        msg=('no such user')
        status=False
        return status,msg

        # print (acc_dic)
        # user_in_db=acc_dic.get(username)
        # if user_in_db:
        #     if int(password)==user_in_db.get('password'):
        #         msg=('pass authentication')
        #         status=True
        #     else:
        #         msg=('wrong  password')
        #         status=False
        # else:
        #     msg=('no such user')
        #     status=False
        # return status,msg


class engine_mysql():
    def auth(self):
        print('mysql-------')





def authentication(user,passwd):
    engine_obj=fetch_account()
    return engine_obj.auth(user,passwd )

