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
channel = "#chlor"
botnick = "protobot_"
buf = ""

s = socket.socket()
s.connect((server, port))
ssock = ssl.wrap_socket(s)

t0 = int(time.time()) # start timesamp
ssock.send(bytes("NICK %s\r\n" % botnick, "UTF-8"))
ssock.send(bytes("USER %s %s blah :%s\r\n" % (botnick, server, botnick), "UTF-8"))

# included
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
  fh = open('u.txt')
  for line in fh:
    ssock.send(bytes("NOTICE %s :%s\n" % (channel, line), "UTF-8"))
  fh.close()

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
    t1 = int(time.time()) # prevent flood
    if(t1 - t0) > 5:
      major()
      t0 = t1

  if(out.find("!die")) != -1:
    ssock.send(bytes("QUIT :Killed by services\r\n", "UTF-8"))
