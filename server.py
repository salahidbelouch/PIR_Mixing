#!/usr/bin/python           # This is server.py file          
# # coding=utf-8
                                                                                                                                                                 

import socket               # Import socket module
import _thread as thread
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor
 
# Function to create the
# random binary string key
def rand_key(n):
   

    key= ""

    for i in range(n):

        temp = str(random.randint(0, 1))
        key += temp
         
    return(key)

# one key of multipiple Bytes 

def rand_key_bytes(b):
    res=''
    for i in range(b):
        if i==b-1:
            res=res+rand_key(8)
        else:
            res=res+rand_key(8)+' '
    return res

#Shares keys with participants 

def keySharing(participants,numbByte):
   numberParticipant=len(participants)
   #on peut avoir plus de deux clès secrete par participant ca augmente l anonymat
   for i in range(numberParticipant):
      print(i)
      participants[i].send((str(numberParticipant)).encode())
   for i in range(numberParticipant):
      #une clef partagée entre deux participants 
      secret_key=rand_key_bytes(numbByte)
      print(i,(i+1)%numberParticipant,secret_key)
      participants[i].send(secret_key.encode())
      participants[(i+1)%numberParticipant].send(secret_key.encode())

def on_new_client(clientsocket,all):
   print("thread handling connection")
   i=1
   while i<=len(all):
      msg = clientsocket.recv(1024)
      print ( 'from >> ', msg)
      #Broadcast:
      for client in all:
         if client != clientsocket :
            client.send(msg)
      i=i+1
   #clientsocket.close()



def  connInit() :
   s = socket.socket()         # Create a socket object
   host = socket.gethostname() # Get local machine name
   port = 1679                # Reserve a port for your service.

   print ('Server started!')
   print ('Waiting for clients...')

   s.bind((host, port))        # Bind to the port
   s.listen(5)                 # Now wait for client connection.

   clients =[]
   last ='no'
   while last == 'no':
      c, addr = s.accept()
      print ('Got connection from', addr)
      clients.append(c)
      last=(c.recv(1024)).decode("utf-8") 
   return s,clients

def padding_ordr(n):
   ord=str(n)
   if len(ord)<4:
      for i in range(4-len(ord)):
         ord=ord+"."
   return ord

def ordre(n):
    ordre=[]
    for i in range (n):
        ordre.append(i)
    random.shuffle(ordre)
    return ordre 

def ordre_sharing(all):
   ordreP=ordre(len(clients))
   i=0
   for client in all:
      #Padding ordre 
      client.send(padding_ordr(ordreP[i]).encode())
      i+=1


#MAIN 
canal,clients =connInit()
keySharing(clients,int(input('bytes?')))
#ordrePassage=ordre(len(clients))
ordre_sharing(clients)
time.sleep(3)
threads=[]

for i in range(len(clients)) :
   threads.append(threading.Thread(target=on_new_client,args=(clients[i],clients,)))

for th in threads:
   th.start()


for th in threads:
   th.join()   
#for i in range(len(clients)-1): 
#   thread.start_new_thread(on_new_client,(clients[i],clients,))
#thread.start_new_thread(on_new_client,(clients[len(clients)-1],clients,))
#while True:
#   i=0
