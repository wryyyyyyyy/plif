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
	# потоки или потомки?
       вот в чем главный вопрос
=========================================
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
srvrname = 'freenode.net'
realname = 'Cool Story Bro'


def ping():
  ircsock.send('PONG :chat.freenode.net' + 'n')

def sendmsg(chan , msg):
  ircsock.send('PRIVMSG ' + chan + ' :'+ msg + 'n')

def joinchan(chan):
  ircsock.send('JOIN ' + chan + 'n')
  ircsock.send('PRIVMSG ' + channel + ' :Консолька, ищи ботов' + 'n') #> onjoin message

"""
 def topic(chan):
 tpc = [ircmsg] for items in tpc:
 print(items)
 ircsock.send("PRIVMSG "+ channel + " :"+ "" +"\n")
"""

def wat():
  ircsock.send('PRIVMSG ' + channel + ' :Да он же у вас однопоточный!' + 'n') #> иногда даже работает

def f_():
  fh = open('u.txt')
  for line in fh:
    #print(line.rstrip()) # можно смотреть в сосноль
    ircsock.send('NOTICE ' + channel + ' :' + line + 'n')
  fh.close()

# иногда не срабатывает функция выше. может дело в регэкспе,
# или сокету явно чего-то не хватает. поэтому пробуем это решение

ircsock.send('rn')

#>==================================================# > try to connect < #================================================= >
## init socket and try to connect ##		      # try to connect < #
						      # Nice Lok

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # wow! we got a socket handle
s.connect((server, port)) 			      # try to connect our network
ircsock = ssl.wrap_socket(s)			      # it should be more secure
url = ('USER ' + username + ' ' + hostname + ' ' + srvrname + ' :' + realname + 'n' )
ircsock.send(bytes(url.encode()))		      # эта строка успешно отослана
url = ('NICK ' + botnick + 'n')			      # подготовим другую,закончим ее 
ircsock.send(bytes(url.encode()))		      # затем отошлем по тому же адресу

while 1:					      # войдем в цикл
ircmsg = ircsock.recv(2048)			      # выделим размер буфера
ircmsg = ircmsg.strip('nr')			      # вырежем симводы переноса строки
print(ircmsg)					      # и выведем пользователю

if(ircmsg.find('376')) != -1: 		      	      # END of /MOT
						      # JOIN CHANNEL
						      # 
if(ircmsg.find(':xzibit:')) != -1:                    #
    wat()					      #
						      #
						      #
  if(ircmsg.find(':Майор, улиточку')) != -1:          #
		
    f_()


  if(ircmsg.find('PING :')) != -1:
    ping()


# EOF
