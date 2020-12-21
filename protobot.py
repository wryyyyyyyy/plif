#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    ============
    PrototypeBot
    ============


"""

import sys
import socket
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
