#!/usr/bin/env bash

nohup python ftp_server.py start &

echo $! > /var/run/ftp.pid

