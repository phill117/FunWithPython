#!/usr/bin/python3

import requests, time, sys

# --------------------------------------------------------------------------

def safeAssign(str, xth):
	try:
		num = int(str)
		if num <= 0: raise ValueError('')
		return num
	except ValueError:
		print("Please provide a positive integer as %dth argument" % (xth))
		exit()

# --------------------------------------------------------------------------

def yo(username):
	res = requests.post("http://api.justyo.co/yo/", 
          data={
              'api_token': 'IM NOT GOING TO PUSH MY API TOKEN AGAIN, GET ONE YOURSELF!!!',
              'username': username.upper()
          }
	)
	print(res.status_code)

# --------------------------------------------------------------------------

# target, times (default = 100), interval (default = 1 sec)

if len(sys.argv) == 1: 
	print("Provide target yo username as first argument.")
	exit()

target = ''
times = 100
interval = 1

i = 1
while (i < len(sys.argv)):
	if i == 1: target	= sys.argv[i] 
	if i == 2: times 	= safeAssign(sys.argv[i], 2)
	if i == 3: interval = safeAssign(sys.argv[i], 3)
	i += 1

yo(target)
for x in range(1, times):
	time.sleep(interval)
	yo(target)
