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
import re
import json
import xml.etree.ElementTree as et
from datetime import datetime

## vars ##
server = "chat.freenode.net"
port = 6697
channel = "#warbot"
botnick = "protobot_"
buf = ""

## defs ##
s = socket.socket()
s.connect((server, port))
ssock = ssl.wrap_socket(s)

## connect ##
_st = int(time.time())  # start time
_stt = _st
kd = 5                  # cooldown
ssock.send(bytes("NICK %s\r\n" % botnick, "UTF-8"))
ssock.send(bytes("USER %s %s %s :%s\r\n" % (botnick, botnick, server, botnick), "UTF-8"))

# included
ul = ('''
я — морская   @             _________
улиточка       \____       /         \\
        \      /    \     /   ____    \\
               \_    \   /   /    \    \\
                 \    \ (    \__/  )    )
                  \    \_\ \______/    /
                   \      \           /___
                    \______\_________/____-_
''')

### УЛИТОЧКА ###
def major():
  for line in ul.splitlines():
    ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, line), "UTF-8"))

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
    ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, out), "UTF-8"))

######### HABR #########
def tcount():
  for node in tree.iter('title'):
    title = node.attrib.get('text')
    _t.append(node)
  return(_t)

def lcount():
  for node in tree.iter('guid'):
    guid = node.attrib.get('text')
    _l.append(node)
  return(_l)


def dcount():
  for node in tree.iter('pubDate'):
    pdate = node.attrib.get('text')
    _d.append(node)
  return(_d)


def rcount():
  for node in tree.iter('description'):
    desc = node.attrib.get('text')
    _r.append(node)
  return(_r)

def core(tree):
  _x = 0
  _dbt = []
  _dbl = []
  _dbd = []
  _dbr = []
  _data = {'Title':'','Date':'','Link':'','Desc':''}

  for t in tree.iter(tag = 'title'): # going throw titles
    _dbt.append(t.text)

    for l in tree.iter(tag = 'guid'): # going throw permlinks
      _dbl.append(l.text)

      for d in tree.iter(tag = 'pubDate'): # going throw date
        _dbd.append(d.text)

        for r in tree.iter(tag = 'description'): # going throw texts
          _dbr.append(r.text)

  _lt = len(_dbt) # get array length

  for t in tree.iter(tag = 'title'):
    if(_x+2 < _lt - 2):
      _out = _dbt[_x+2]+' | '+_dbl[_x]+' | '+_dbd[_x]
      ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, _out), "UTF-8"))
      _x = _x + 1
      time.sleep(1)
    else:
      break

## init ##
def habr():
  url = "https://habr.com/ru/rss/all/?fl=ru"
  res = requests.get(url)
  tree = et.fromstring(res.content)

  _t = []
  _l = []
  _d = []
  _r = []
  core(tree)
####################

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

### HELPME ###
def helpme():
  out = "`help | `starttime | `utctime | `xkcd | `habr | `iss | [М,м]айор, улиточку | `botcode | `die"
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

    if(line[1] == "366"): # End of /NAMES
      ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, "Feel free to type `help | Botcode available at: https://t1p.de/ix4u"), "UTF-8"))

    if(line[0] == "PING"): # KIM CHEN PONG d[^__|__^]b
      ssock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))

### УЛИТОЧКА ###
  out = str(tmp)
  if(out.find("Майор, улиточку")) != -1: #) or
    _now = int(time.time())
    if(_now > _stt + kd):
      major()
      _stt = _now
  elif(out.find("майор, улиточку")) != -1:
    _now = int(time.time())
    if(_now > _stt + kd):
      major()
      _stt = _now

### STARTTIME ###
  if(out.find("`starttime")) != -1:
    _now = int(time.time())
    _u = datetime.utcfromtimestamp(_st)
    if(_now > _stt + kd):
      ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, "Bot online since:\t"+str(_u)), "UTF-8"))
      _stt = _now

### BOTTIME ###
  if(out.find("`utctime")) != -1:
    _now = int(time.time())
    _u = datetime.fromtimestamp(_now)
    _utc = datetime.utcnow() # UTC datetime now
    _n = _utc.timestamp() # from _utc

    _nyc = _n-5*60*60
    _nyc = datetime.fromtimestamp(int(_nyc))
    _lnd = _n+0*60*60
    _lnd = datetime.fromtimestamp(int(_n))
    _prs = _n+1*60*60
    _prs = datetime.fromtimestamp(int(_prs))
    _msc = _n+3*60*60
    _msc = datetime.fromtimestamp(int(_msc))
    _pek = _n+8*60*60
    _pek = datetime.fromtimestamp(int(_pek))
    _tok = _n+9*60*60
    _tok = datetime.fromtimestamp(int(_tok))
    _laa = _n+16*60*60
    _laa = datetime.fromtimestamp(int(_laa))

    _ts =  "Current UTC time: "+_utc.strftime("%H:%M:%S")+" | NYC: "+_nyc.strftime("%H:%M")+" | London: "+_lnd.strftime("%H:%M")+" | Paris: "+_prs.strftime("%H:%M")+" | Moscow: "+_msc.strftime("%H:%M")+" | Peking: "+_pek.strftime("%H:%M")+" | Tokyo: "+_tok.strftime("%H:%M")+" | LA: "+_laa.strftime("%H:%M")

    if(_now > _stt + kd):
      ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, _ts), "UTF-8"))
      _stt = _now

### BOTCODE ###
  if(out.find("`botcode")) != -1:
    _now = int(time.time())
    if(_now > _stt + kd):
      url = "https://t1p.de/ix4u"
      ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, url), "UTF-8"))
      _stt = _now

### SHUTDOWN ###
  if(out.find("`die")) != -1:
    #ssock.send(bytes("QUIT :Killed by services\r\n", "UTF-8"))
    ssock.send(bytes("NOTICE %s :%s\r\n" % (channel, "Will be enabled soon :3"), "UTF-8"))
    #quit() # Quit programm

### XKCD ###
  if(out.find("`xkcd")) != -1:
    _now = int(time.time())
    if(_now > _stt + kd):
      xkcd()
      _stt = _now

### HABR ###
  if(out.find("`habr")) != -1:
    _now = int(time.time())
    if(_now > _stt + kd):
      habr()
      _stt = _now

### ISS TRACKER ### TOP SECRET ### USING FOR KGB AGENTS ONLY ###
  if(out.find("`iss")) != -1:
    _now = int(time.time())
    if(_now > _stt + kd):
      iss()
      _stt = _now

### HELPME ###
  if(out.find("`help")) != -1:
    _now = int(time.time())
    if(_now > _stt + kd):
      helpme()
      _stt = _now
