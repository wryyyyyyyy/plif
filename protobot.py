#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    ============
    PrototypeBot
    ============


"""
import sys
import socket
import time
import ssl

## vars ##
server = "chat.freenode.net"
port = 6697
channel = "#warbot"
botnick = "protobot_"
buf = ""

s = socket.socket()
s.connect((server, port))
ssock = ssl.wrap_socket(s)

ssock.send(bytes("NICK %s\r\n" % botnick, "UTF-8"))
ssock.send(bytes("USER %s %s blah :%s\r\n" % (botnick, server, botnick), "UTF-8"))

ul = '''
я — морская   @             _________
улиточка       \____       /         \
        \      /    \     /   ____    \
               \_    \   /   /    \    \
                 \    \ (    \__/  )    )
                  \    \_\ \______/    /
                   \      \           /___
                    \______\_________/____-_
'''

def major():
  #print(ul)
  #ssock.send(bytes("PRIVMSG %s :%s\n" % (channel, ul), "UTF-8"))
  fh = open('u.txt')
  for line in fh:
    ssock.send(bytes("PRIVMSG %s :%s\n" % (channel, line), "UTF-8"))
  fh.close()
  cooldown() # some antiflood routine shall be implemented here

def cooldown():
  time.sleep(5)

while 1:
  buf = buf+ssock.recv(1024).decode("UTF-8")
  tmp = str.split(buf, "\n")
  buf=tmp.pop()

  for line in tmp:
    print(line) ## FOR VISUAL IRC CONTROL ##
    line = str.rstrip(line)
    line = str.split(line)

    if(line[1] == "376"): # END OF /MOTD
      ssock.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))

    if(line[0] == "PING"):
      ssock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))

  out = str(tmp)
  if(out.find("Майор, улиточку")) != -1:
    major()
