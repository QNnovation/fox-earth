#!/usr/bin/env python3

import socket
import json

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto = 0)
serv_sock.bind(('', 49111))
serv_sock.listen(10)


print("TCP Server started at port number: " + str(49111))

while True:
	client_conn, client_addr = serv_sock.accept()
	print("Connected by", client_addr)
	raw_data = b''

	while True:
		tmp = client_conn.recv(1024)
		if not tmp:
			break
		raw_data += tmp
		data = json.loads(raw_data.decode('utf-8'))
		print(data)
		client_conn.sendall(b'Connection close')
client_conn.close()