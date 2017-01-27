#!/usr/bin/env bash

nohup python ftp_server.py start &> /dev/null 2>&1 &

echo $! > /var/run/ftp.pid

