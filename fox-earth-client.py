#!/usr/bin/env python3

import psutil, sys
import socket
import ipaddress
import json

# Data;
_argLen = len(sys.argv)
_port	= '49111'

# JSON;
_data = {'data':{'ipaddress': '127.0.0.1', 'command': 'empty'}}


# Validate ip address;
def _ipAddrValidate(ipAddr):
	try: 
		ipaddress.ip_address(ipAddr)
		return True
	except ValueError as errorCode:
		print("Error: invalid input ip address entered!")
		return False

def getUsage():
    print("Usage:\n$./fox-earth-client.py LATER")

#-----------------------------------------------------------------#

if _argLen == 3:
    if sys.argv[1] == "-s":
    	if _ipAddrValidate(sys.argv[2]):
    		_data['data']['ipaddress'] = sys.argv[2] 
    	else:
    		getUsage()

elif _argLen == 4:
	if sys.argv[1] == "-s":
		if sys.argv[3] == "--get-settings":
			if _ipAddrValidate(sys.argv[2]):
				_data['data']['ipaddress'] = sys.argv[2] 
				_data['data']['command'] = sys.argv[3]
			else:
				getUsage()
else:		     
	getUsage()


# Connect to server;
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((_data['data']['ipaddress'], int(_port)))

# Send data to server;
raw_data = json.dumps(_data).encode('utf-8')
client_sock.sendall(raw_data)


# Answer from server;
reply = client_sock.recv(1024)
print("Received: ", reply)
client_sock.close()
