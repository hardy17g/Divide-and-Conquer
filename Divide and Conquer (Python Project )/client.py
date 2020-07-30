import json
import socket
import time
s = socket.socket()
host = '159.89.168.164'
port = 12345
s.connect((host, port))
print("Connection Established")
s.send("Hardik".encode())
def send_string(d):
    s.send(d.encode())
    print("send")
def receive_string(user):
	while True:
		try:
			data = s.recv(1024)
			#print(data.decode('utf-8'))
			if len(data.decode('utf-8'))>0:
				print(data.decode('utf-8'))
				d = json.loads(data.decode('utf-8'))
				if user == d['user']:
					print(d)
					return d
					
				else:
					continue	 
		except socket.error as err:
			print(err)
			return None
			#print(data.decode('utf-8'))
#{"user": "Utkarsh", "day": "19", "month": "11", "year": "2019", "time": "01:50:57", "expen": 111.0, "split": 0, "cat": "Transport", "split_dictionary": {"user": "Utkarsh", "returnFrom": {}, "owedTo": {"Hardik": 111.0}}, "comments": "uber"}
#{"user":"Hardik","day":10,"month":11,"year":19,"time":10,"expen":270,"split":0,"cat":"category","split_dictionary":{"user":"Hardik","returnFrom":{},"owedTo":{}},"comments":""}
#{"user":"Utkarsh","day":10,"month":11,"year":19,"time":10,"expen":270,"split":0,"cat":"category","split_dictionary":{"user":"Hardik","returnFrom":{},"owedTo":{}},"comments":""}