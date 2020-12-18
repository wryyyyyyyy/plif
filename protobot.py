#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

    ============
    PrototypeBot
    ============


"""

import os
import sys
import socket
import random
import time
import ssl


"""
# will be threaded or fork() a bit later. maybe #
#def parent_child():
  #n = os.fork()

  # n greater than 0  means parent process
  #if n > 0:
    #print("Parent PID : ", os.getpid())

  # n equals to 0 means child process
  #else:
    #print("Child PID : ", os.getpid())

# Driver code
#parent_child()
"""



server = 'chat.freenode.net'
port = 6697
channel = '#warbot'
botnick = 'YourBro'

username = 'Not Your Bro'
hostname = 'chat.freenode.net'
servername = 'freenode.net'
realname = 'Cool Story Bro'


def ping():
  ircsock.send('PONG :chat.freenode.net' + 'n')

def sendmsg(chan , msg):
  ircsock.send('PRIVMSG ' + chan + ' :'+ msg + 'n')

def joinchan(chan):
  ircsock.send('JOIN ' + chan + 'n')
  ircsock.send('PRIVMSG ' + channel + ' :Консолька, ищи ботов' + 'n') # onjoin message

# def topic(chan):
# tpc = [ircmsg] for items in tpc:
# print(items)
# ircsock.send("PRIVMSG "+ channel + " :"+ "" +"\n")

def wat():
  ircsock.send('PRIVMSG ' + channel + ' :Да он же у вас однопоточный!' + 'n') # иногда даже работает

def f_():
  fh = open('u.txt') # улиточка в ASCII
  for line in fh:
    #print(line.rstrip()) # можно смотреть в сосноль
    ircsock.send('NOTICE ' + channel + ' :' + line + 'n')
  fh.close()
  
  ircsock.send('rn') # иногда не срабатывает
		     # улиточка. или дело в регэкспе,
		     # или сокету явно чего-то не хватает

# ================================================== #
## try to connect ##
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
ircsock = ssl.wrap_socket(s)
url = ('USER ' + username + ' ' + hostname +' '+ servername +' :'+ realname + 'n')
ircsock.send(bytes(url.encode()))
url = ('NICK ' + botnick + 'n')
ircsock.send(bytes(url.encode()))

while 1:
  ircmsg = ircsock.recv(2048)
  ircmsg = ircmsg.strip('nr')
  print(ircmsg)

  if(ircmsg.find('376')) != -1: # :END of /MOTD +
    joinchan(channel)           # JOIN CHANNEL


  if(ircmsg.find(':xzibit:')) != -1:
    wat()


  if(ircmsg.find(':Майор, улиточку')) != -1:
    f_()


  if(ircmsg.find('PING :')) != -1:
    ping()


### EOF ###
