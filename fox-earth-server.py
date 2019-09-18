#!/usr/bin/env python3

import socket
import json
from sysInfo import GetNetworkInfo

# All interafaces listening;
HOST = 'localhost'
PORT = 49111

print('[Starting TCP server]')

# Connect to server;
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((HOST, PORT))
	sock.listen(10)

	while True:
		conn, addr = sock.accept()
		# Get input server input ip address, from where packet in;
		_inputAddress = conn.getsockname()[0]
		with conn:
			print('Connected by ', addr)
			full_data = b''
			while True:
				data = conn.recv(1024)
				if not data: break
				# Collect all data;
				full_data += data
				# Check for end of data transmit;
				if 'end' in data.decode('utf-8'):
					full_data = full_data.decode('utf-8').replace('end', '')
					break;
			print('Full data: ', full_data)
			# Convert input data to JSON;
			data = json.loads(full_data)
			# Check JSON data;
			if data['data']['command'] == '--get-settings':
				# Create GetNetwork info class to get network information;
				_netInfo = GetNetworkInfo()
				nicInfoDict = _netInfo.getNicInfo(_inputAddress)
			else:
				print("No input options from client!")
				conn.send(b'error')
				break

    		# Send data to client;
			raw_dataJSON = json.dumps(nicInfoDict).encode('utf-8')
			print('Dictionary: ', raw_dataJSON)
			print(f'Size of transmited message: {len(raw_dataJSON)} bytes.')
			conn.send(raw_dataJSON)
			# Send end of data sign;
			conn.send(b'end')
			print("Transmit data finished!")
