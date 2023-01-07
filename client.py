#!/usr/bin/python           # This is client.py file

from ast import While
import socket               # Import socket module
import _thread as thread
import random
import string
import threading
import timeit

  

class participant:
  def __init__(self,name,msg,last):
    self.name = name
    self.msg = msg
    self.keys=[]
    self.last=last
    self.ordre=[]

def generateur(n):
    letters = string.ascii_lowercase
    return (''.join(random.choice(letters) for i in range(n)) )
    

def tailleAttendue(Byte):
    return (Byte*9-1)

def keystoArr(keys):
    res=[]
    byte=''
    for i in range(len(keys)):
        if keys[i]!=' ':
            byte=byte+keys[i]
        else:
            res.append(byte)
            byte=''
    res.append(byte)
    return res

def receive_keys(part,conn,taille):
    part.keys.append(keystoArr(conn.recv(tailleAttendue(taille)).decode("utf-8")))
    part.keys.append(keystoArr(conn.recv(tailleAttendue(taille)).decode("utf-8")))

def arraytoStr(msgArray):
    res=''
    for i in range(len(msgArray)):
        if i==len(msgArray)-1:
            res=res+msgArray[i]
        else:
            res=res+msgArray[i]+' '
    return res

def utf8len(s):
    return len(s.encode('utf-8'))

def prepare_message(msg,keys):
    res=[]
    intermediaire=[]
    #add padding
    byteTotal=len(keys[0])
    msgBinaire=toBinary(msg,byteTotal)
    #print("le message en binaire",msgBinaire)
    #Si keys non binaires
    #key1=(' '.join(format(ord(x), 'b') for x in keys[0]))
    #key1=(' '.join(format(ord(x), 'b') for x in keys[1]))
    msgBinaire=padding(msgBinaire)
    #print("le meessage binaire après padding",msgBinaire)


    for i in range(len(keys[0])):
        y=int(msgBinaire[i], 2)^int(keys[0][i],2)
        intermediaire.append((bin(y)[2:].zfill(len(msgBinaire[i]))))
            #intermediaire+=str(int(msgBinaire[i])^(int((keys[0][i]))))
    for i in range(len(keys[0])):
        y=int(intermediaire[i], 2)^int(keys[1][i],2)
        res.append(bin(y)[2:].zfill(len(msgBinaire[i])))
    return res

def padding(binaire):
    res=[]
    for byte in binaire:
        if len(byte)<8:
            for i in range(8-len(byte)):
                byte="0"+byte
        res.append(byte)
    return res

def toBinary(a,n):
    l,m=[],[]
    if a=='':
        for i in range(n):
            m.append('00000000')
    else:
        for i in a:
            l.append(ord(i))
        for i in l:
            m.append((bin(i)[2:]))
    return m

def envoie(noeud,message,conn):
    msg_pret=prepare_message(message,noeud.keys)
    conn.send(arraytoStr(msg_pret).encode())
    #print("I sent ", msg_pret)
    return msg_pret

def one_slot(n,conn,taille,msg_env):
    total_msg=[msg_env]
    for i in range(n-1):        
     received=conn.recv(taille).decode("utf-8")   
     #print("received",(received))
     total_msg.append(keystoArr(received))
    return total_msg

def binaryToStr(binary_values):
    ascii_string = ""
    for binary_value in binary_values:
        an_integer = int(binary_value, 2)



        ascii_character = chr(an_integer)

        ascii_string += ascii_character
    return ascii_string

def xor(A,B):
    res=[]
    for i in range(len(A)):
            y=int(A[i], 2)^int(B[i],2)
            res.append((bin(y)[2:].zfill(8)))
    return res


def decodage_msg(total,r):
    res=[]
    res=xor(total[0],total[1])
    for i in range(2,len(total)):
        res=xor(res,total[i])
    print("round:",r,"message :",binaryToStr(res) )
    
def receive_ordre(part,nombreP,conn):
    
    #ord=int((conn.recv(tailleAttendue(utf8len(str(nombreP))))).decode("utf-8"))
    ordrstr=(conn.recv(4)).decode("utf-8")
    ord=int((ordrstr.split("."))[0])
    for i in range(nombreP):
        if i==ord:
            part.ordre.append(1)
        else:
            part.ordre.append(0)

def co_participant(noeud,nb):
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 1679              # Reserve a port for your service.
    s.connect((host, port))
    #print(s.recv(1024))

    
    s.send((noeud.last).encode())
    n_participants=int(s.recv(1).decode("utf-8"))

    print(n_participants)   #print////

    receive_keys(noeud,s,nb)

    print(noeud.keys[0],noeud.keys[1])  #print////

    receive_ordre(noeud,n_participants,s)
    print("mon ordre ", noeud.ordre)

    for i in range(n_participants):
        if noeud.ordre[i]!=1:
            msg=''
        else:
            msg=noeud.msg
        
        msg_envoye=envoie(noeud,msg,s)
        total_m=one_slot(n_participants,s,tailleAttendue(len(noeud.keys[0])) ,msg_envoye)
        #print(total_m)
        decodage_msg(total_m,i)
    #s.close()


#MAIN
nb = int(input ( "nombre noeud"))
byte = int(input ( "nombre byte"))
#passage1=[[1,0,0],[0,1,0],[0,0,1]] 

#for i in range(nb-1):
#    thread.start_new_thread(co_participant,(participant(str(i),generateur(byte),'no'),byte,))
#co_participant(participant('A',input('msg?'),input('last?')),byte)


threads=[]
for i in range(nb-1):
   threads.append(threading.Thread(target=co_participant,args=(participant(str(i),generateur(byte),'no'),byte,)))


start = timeit.default_timer()

for th in threads:
   th.start()
co_participant(participant('last',input('msg?'),input('last?')),byte)

for th in threads:
   th.join()

stop = timeit.default_timer()

print('Time: ', stop - start)

