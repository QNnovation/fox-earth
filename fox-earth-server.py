#!/usr/bin/env python3

import socket
import json
from sysInfo import GetNetworkInfo

_port = 49111

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto = 0)
serv_sock.bind(('', _port))
serv_sock.listen(10)

def dictToJSON(dict):
	pass


# Create GetNetwork info class to get network information;
_netInfo = GetNetworkInfo()

while True:
	clientsocket, address = serv_sock.accept()
	print("[TCP Server started at port number: " + str(_port) + ']')
	# Get input server input ip address, from where packet in;
	_inputAddress = clientsocket.getsockname()[0]
	
	# Input info, for debug purposes;
	print("[Server input ip address: " + str(_inputAddress) + ']')
	print(f'[Connection from {address} has been established!]')
	
	# Get data from client;
	full_data = ''
	while True:
		data = clientsocket.recv(1024)
		if not data:
			break
		full_data += data.decode('utf-8')
		
	print('DEBUG')
	# Convert input data to JSON;
	data = json.loads(full_data)
		
	if data['data']['command'] == '--get-settings':
		nicInfo = _netInfo.getNicInfo(_inputAddress)
		print("Information: " + str(nicInfo))
	else:
		print("else")
			

	# Send data to client;
	raw_data = json.dumps(nicInfo).encode('utf-8')
	
	clientsocket.send(raw_data)
	print("Data send!")
	clientsocket.close()
