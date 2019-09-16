#!/usr/bin/env python3

import netifaces
from accessify import private


# Class implementation;

class GetNetworkInfo(object):
	def __init__(self):
		self.__nicInfo = {'iface_name': '',
							'ip': [],
							'netmask': [],
							'gw': '',
							'dns': ''}
	
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
			self.__nicInfo['dns'] = 'empty'

		#print(self.__nicInfo)
		return self.__nicInfo
		
#obj = GetNetworkInfo()
#obj.getNicInfo('127.0.0.1')
