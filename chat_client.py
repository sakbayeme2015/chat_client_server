#!/usr/bin/env python 

import sys
import select 
import socket 

if len(sys.argv) <3:
 print "Usage : chat_client.py <address> <port>"
 exit()

def chat_client():

 host = sys.argv[1]
 socket_list = []
 port = int(sys.argv[2])

 sock_object = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
 sock_object.settimeout(2)
 try:
  sock_object.connect((host,port))
 except:
  print "Unable to connect"
  exit()
 print "connect to remote host you can start send message" 
 sys.stdout.write('[>]'); sys.stdout.flush()

 while 1:
  socket_list = [sys.stdin , sock_object] 
  read_object , write_object, in_error = select.select(socket_list , [],[]) 
  
  for sock in read_object:
   if sock == sock_object:
    data = sock.recv(4096)
    if not data:
     print '\nDisconnected from chat server'
     exit()
    else:
     sys.stdout.write(data)
     sys.stdout.write('[>]'); sys.stdout.flush()
   else:
    msg = sys.stdin.readline() 
    sock_object.send(msg)
    sys.stdout.write('[>]'); sys.stdout.flush()

chat_client()

 
   
   
 
 

