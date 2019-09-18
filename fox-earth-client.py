#!/usr/bin/env python3

import sys
import socket
import ipaddress
import json

# Data;
HOST = 'localhost'
PORT = 49111

_argLen = len(sys.argv)

# JSON;
_data = {'data':{'ipaddress': 'null', 'command': 'null'}}

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

# Check for input command arguments;
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

print('[Starting TCP client]')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.connect((_data['data']['ipaddress'], PORT))
	# Send data to server;
	raw_data = json.dumps(_data).encode('utf-8')
	sock.send(raw_data)
	# Send end of data sign;
	sock.send(b'end')

	# Get data from server;
	print("Get data from server...")
	full_data = b''
	while True:
		data = sock.recv(1024)
		if not data:
			break
		# Check for error;
		if 'error' in data.decode('utf-8'):
			print('Client send bad options!')
			break

		full_data += data
		# Check for end of data transmit;
		if 'end' in data.decode('utf-8'):
			full_data = full_data.decode('utf-8').replace('end', '')
			break;

	# Convert input data to JSON;
	if full_data:
		print("Received data from server ->\n", full_data)
		data = json.loads(full_data)
		print("Unpacked data reply from server ->\n ", data)
