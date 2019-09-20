#!/usr/bin/env python3

import socket
import ipaddress
import json
import argparse

# Data;
HOST = 'localhost'
PORT = 49111

# Create the argv parser;
argv_parser = argparse.ArgumentParser(description='TCP client for remote connection')

# Add the arguments;
argv_parser.add_argument('Source',
						metavar='source',
						type=str,
						help='the ip address of remote server')
argv_parser.add_argument('--get-settings',
						action='store_true',
						help='get server network interface options')

_args = argv_parser.parse_args()


# JSON;
_data = {'data':{'ipaddress': 'null', 'command': 'null'}}


# Validate ip address;
def _ipAddrValidate(ipAddr):
	try:
		ipaddress.ip_address(ipAddr)
		return True
	except ValueError as errorCode:
		print("[Network error: invalid input ip address entered]")
		return False


# Check for input command arguments;
def _getCliArgs():
	if _args.get_settings:
		if _ipAddrValidate(_args.Source):
			_data['data']['ipaddress']	= _args.Source
			_data['data']['command']	= '--get-settings'
			return True
		else:
			return False


print('[Starting EARTH TCP client]')


if _getCliArgs():

	# Exception 1
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		# Exception 2
			try:
				sock.connect((_data['data']['ipaddress'], PORT))
				# Send data to server;
				raw_data = json.dumps(_data).encode('utf-8')
				print("[Log: bytes sended %d]" % sock.send(raw_data))
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
			except socket.gaierror as err:
				print('[Network error: address related error connecting to server. %s]' % err)
	except socket.error as err:
		print('[Network error: can\'t create socket. %s]' % err)
