#!/usr/bin/env python
# -*- coding=utf8 -*-

import sys, tty, termios

def getch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch
def getpass(maskchar = "*"):
  password = ""
  while True:
    ch = getch()
    if ch == "\r" or ch == "\n":
      print
      return password
    elif ch == "\b" or ord(ch) == 127:
      if len(password) > 0:
        sys.stdout.write("\b \b")
        password = password[:-1]
    else:
      if maskchar != None:
        sys.stdout.write(maskchar)
      password += ch