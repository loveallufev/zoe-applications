#!/usr/bin/env python

import sys
import requests
import os

EXEC_ID = os.environ['ZOE_EXECUTION_ID']
ZOE_URL = os.environ['ZOE_URL']

r = requests.get('{}/discovery/by_group/{}/all'.format(ZOE_URL, EXEC_ID))
data = r.json()

for name in data['dns_names']:
	if 'storage' in name:
		sys.stdout.write('{} '.format(name))
sys.stdout.write("\n")

