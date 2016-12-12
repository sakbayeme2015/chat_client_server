#!/usr/bin/env python 

import socket 
import select 

host = "0.0.0.0"
socket_list = []
buffer = 4096
port = 60000

def chat_server():

 sock_object = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
 sock_object.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
 sock_object.bind((host , port))
 sock_object.listen(20)
 socket_list.append(sock_object)
 
 print "Chat server start on port " + str(port)

 while 1:
  #read the socket with select 
  read_object,write_object,in_error = select.select(socket_list,[],[],0)

  for sock in read_object:

   if sock == sock_object:
    sockfd,addr = sock_object.accept()
    socket_list.append(sockfd)
    print "Chat (%s,%s) connected" %addr

    broadcast(sock_object , sockfd , "[%s:%s] chat enter all client\n" % addr) 

   else:
    # process data received from client
    try:
     data = sock.recv(buffer)
     if data:
      #there is something in the socket
      broadcast(sock_object , sock , "\r" + '[' + str(sock.getpeername()) +']' + data)
     else:
      #remove the socket that's broken
      if sock in socket_list:
       socket_list.remove(sock)
    except:
     broadcast(sock_object , sock , "Client(%s,%s) is offline \n" % addr )
     continue

 sock_object.close() 


#broadcast chat message to all client 
def broadcast(sock_object , sock , message):
 for socket in socket_list:
  if socket != sock_object and socket != sock:
   try:
    socket.send(message)
   except:
    socket.close()
    if socket in socket_list:
     socket_list.remove(socket) 

chat_server()

