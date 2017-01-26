#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging,os,sys
base_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.append(base_dir)
from config import settings
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler

#是否要打印在屏幕#
is_console = False
#是否要备份日志#
is_backfile = False
#是否写日志#
is_writefile = True

# create file handler and set level to warning
if os.path.exists("%s/logs"%base_dir) is not True:
    os.mkdir("%s/logs"%base_dir)
if settings.log_file:
    logname = '%s/logs/%s'%(base_dir,settings.log_file)
else:
    logname = '%s/logs/ftp.log'%base_dir

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
if is_console:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)
#################################################################################################
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
if is_backfile:
    Rthandler = RotatingFileHandler('%s'%logname,maxBytes=100*1024*1024,backupCount=5)
    Rthandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
    Rthandler.setFormatter(formatter)
    logger.addHandler(Rthandler)
#################################################################################################
#定义一个FileHandler，将INFO级别或更高的日志信息写入日志中#
if is_writefile:
    logfile =  TimedRotatingFileHandler("%s"%logname, "D", 1, 10)
    logfile.suffix = "%Y%m%d"
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s')
    if settings.log_level == "debug":
        logfile.setLevel(logging.DEBUG)
    elif settings.log_level == "info":
        logfile.setLevel(logging.INFO)
    elif settings.log_level == "warning":
        logfile.setLevel(logging.WARNING)
    elif settings.log_level == "error":
        logfile.setLevel(logging.ERROR)
    else:
        logfile.setLevel(logging.ERROR)
    # logfile.setLevel(logging.INFO)
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
