#!/usr/bin/env python3
# Test script;
import json
data = {'iface_name': '',	'ip': [], 'netmask': [], 'gw': '', 'dns': []}
raw_dataJSON = json.dumps(data).encode('utf-8')
print(f'Size of transmited message: {len(raw_dataJSON)} bytes.')
