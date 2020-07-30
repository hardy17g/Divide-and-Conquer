import socket
#import sys
import threading
import time
from queue import Queue
import json
users = {'Utkarsh':None, 'Hardik':None, 'Jaideep':None}
NUMBER_OF_THREADS = 3
JOB_NUMBER = [1, 2, 3]
queue = Queue()
all_connections = []
all_address = []
messages = []
# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 12345
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    '''for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]'''

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout
            user = conn.recv(1024).decode('utf-8')
            users[user] = conn
            all_connections.append(conn)
            all_address.append(address)
            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# Send commands to client/victim or a friend
def send_string ():
    global messages
    i = 0
    while i<len(messages):    
        for x in messages[0]:
            try:
                users[x['user']].send(json.dumps(x).encode())
                print(users[x['user']].getpeername())
                print("send")
            except:
                print("could not send the string")
        messages.pop(0)
# receive string
def receive_string():
    global messages
    for conn in all_connections:
        try:
            d = conn.recv(1024)
            if len(d.decode('utf-8'))>0:
                messages.append(json.loads(d.decode('utf-8')))
                print(messages)   
        except :
            print("Error in receiving string")
            continue
        
        #messages = [ ]

# Create worker threads
def create_workers():
    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            while True:
                receive_string()
        if x == 3:
            while True:
                send_string()    
        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()