#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    ============
    PrototypeBot
    ============

"""

import sys
import socket
import requests
import time
import ssl
import xml.etree.ElementTree as et
import json
from datetime import datetime

## vars ##
server = "chat.freenode.net"
port = 6697
channel = "#warbot"
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

### УЛИТОЧКА ###
def major():
  fh = open('u.txt')
  for line in fh:
    ssock.send(bytes("NOTICE %s :%s\n" % (channel, line), "UTF-8"))
  fh.close()

### XKCD ###
def xkcd():
  url = "https://xkcd.com/rss.xml"
  res = requests.get(url)
  tree = et.fromstring(res.content)
  title = tree.findall('channel/title/item')
  cnt = tree.findall('.//title') #count titles
  l = len(cnt)

  for j in range(l):
    out = ""
    cnt = tree.findall('.//title')
    if j < l-1:
      out = out + cnt[j+1].text + " | "

    cnt = tree.findall('.//link')
    if j < l-1:
      out = out + cnt[j+1].text
    ssock.send(bytes("NOTICE %s :%s\n" % (channel, out), "UTF-8"))

### ISS TRACKER ###
def iss():
  url = "http://api.open-notify.org/iss-now.json"
  res = requests.get(url)
  cnt = (res.content).decode("UTF-8")
  v = json.loads(cnt)
  t = v['timestamp'] # TIME
  c = json.dumps(v['iss_position'],0)
  v = json.loads(c)
  lat = v['latitude']
  lng = v['longitude']
  rt = datetime.fromtimestamp(t)
  out = "Latitude:\t" + str(lat) + " | " + "Longitude:\t" + str(lng) + " | " + "Timestamp:\t" + str(rt) + "\n"
  ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, out), "UTF-8"))


### MAIN LOOP ###
while 1:
### RECIEVE ###
  buf = buf+ssock.recv(1024).decode("UTF-8")
  tmp = str.split(buf, "\n")
  buf=tmp.pop()

### VISUAL IRC CONTROL ###
  for line in tmp:
    print(line)
    line = str.rstrip(line)
    line = str.split(line)

    if(line[1] == "376"): # END OF /MOTD
      ssock.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))

    if(line[0] == "PING"): # KIM CHEN PONG d[^__|__^]b
      ssock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))

### УЛИТОЧКА ###
  out = str(tmp)
  if(out.find("Майор, улиточку")) != -1:
    t1 = int(time.time()) # prevent flood
    if(t1 - t0) > 5:      # cooldown 5 sec.
      major()
      t0 = t1

### BOT STARTTIME ###
  if(out.find("!up")) != -1:
    rt = datetime.fromtimestamp(t0)
    ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, "Bot online since:\t" + str(rt)), "UTF-8"))

### BOT TIMENOW ###
  if(out.find("!now")) != -1:
    tt = int(time.time())
    rt = datetime.fromtimestamp(tt)
    ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, "Current bot time:\t" + str(rt)), "UTF-8"))

### BOT SHUTDOWN ###
  if(out.find("!die")) != -1:
    ssock.send(bytes("QUIT :Killed by services\r\n", "UTF-8"))

### XKCD ###
  if(out.find("!xkcd")) != -1:
    t1 = int(time.time()) # prevent flood
    if(t1 - t0) > 5:      # cooldown 5 sec.
      xkcd()
      t0 = t1

### ISS TRACKER ### TOP SECRET ### USING FOR KGB AGENTS ONLY ###
  if(out.find("!iss")) != -1:
    t1 = int(time.time()) # prevent flood
    if(t1 - t0) > 5:      # cooldown 5 sec.
      iss()
      t0 = t1
