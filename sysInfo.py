#!/usr/bin/env python3

import netifaces
import subprocess
from accessify import private

# Class implementation;

class GetNetworkInfo(object):
	def __init__(self):
		self.__nicInfo = {'iface_name': '',	'ip': [], 'netmask': [], 'gw': '', 'dns': []}
		self.__libList = ['netifaces', 'argparse', 'ipaddress', 'socket', 'accessify', 'netifaces']

	@private
	def __getNicNameByIpAddr(self, ipAddr):
		interfacesList = netifaces.interfaces()
		matchInterface = ''
		for interface in interfacesList:
			ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
			if str(ipAddr) == ip:
				matchInterface = interface
				break
		return matchInterface

	def getNicInfo(self, ipAddr):
		interface = self.__getNicNameByIpAddr(ipAddr)
		if interface:
			optionsLength = len(netifaces.ifaddresses(interface)[netifaces.AF_INET])
			for cnt in range(optionsLength):
				# Nic ip address;
				self.__nicInfo['ip'].append(netifaces.ifaddresses(interface)[netifaces.AF_INET][cnt]['addr'])
				# Nic netmask;
				self.__nicInfo['netmask'].append(netifaces.ifaddresses(interface)[netifaces.AF_INET][cnt]['netmask'])
			# Nic name;
			self.__nicInfo['iface_name'] = interface
			# Nic gateway address;
			self.__nicInfo['gw'] = netifaces.gateways()['default'][netifaces.AF_INET][0]
			# Nic dns adress;
			# Read /etc/resolv.conf
			f = open('/etc/resolv.conf', 'r')
			while True:
				line = f.readline()
				if not line:
					break
				if 'nameserver' in line:
					pos = line.find(' ')
					line = line[pos + 1:].strip()
					self.__nicInfo['dns'].append(line)
			f.close()
		return self.__nicInfo

	def checkForInstalledLibs(self):
		installedLibs = str(subprocess.check_output(["pip3", "list"]))
		for libName in self.__libList:
			if libName not in installedLibs:
				print(str(subprocess.check_output(["pip3", "install", "{}".format(libName)])))


# For test purposes;
#obj = GetNetworkInfo()
#obj.checkForInstalledLibs()
#print(obj.getNicInfo('127.0.0.1'))
