#!/usr/bin/python3

import sys, os, configparser, requests, json, re, random

# TODO: Don't format integer rolls as floats
# TODO: silly messages for natural 20s and 1s
# TODO: some sort of glorious dice rolling sound effects

'''
Push20: a Python3 interface with Pushbullet that allows people to roll dice and push the result to themselves and/or someone else.

Usage:
push20.py [email] [dice]

Arguments:
email:	standard email@something.com format
dice:	standard [N]dX+K, where N is number of dice, X is number of faces of the dice
		+ is the operator (+, -, *|x, /) accepted, K is the factor to operate on

Note: It's been a while since I've done any Python. Sorry in advance.
'''

# Read in command-line arguments; first one is destination, second is dice to roll
# Both are optional, if there is no destination, it'll send to yourself by default
# if there's not dice to roll it'll roll a single d20 by default

# Dice regular expression
DiceRegex = '^([0-9]*)d([0-9]+)([\+\-\*\/x]?)([0-9]*)$'

# default, no arguments
diceString = 'd20'
email = ''

# 2 arguments: check what kind of argument it is
match = None
if len(sys.argv) == 2:
	if '@' in sys.argv[1]:
		email = sys.argv[1]
	else:
		match = re.match(DiceRegex,sys.argv[1])
		if match:
			diceString = sys.argv[1]
		else:
			print("Something's wrong with your arguments.")
			sys.exit()
# 3 args - email dice
elif len(sys.argv) == 3:
	if '@' in sys.argv[1]:
		email = sys.argv[1]
	else:
		print("Invalid email entered.")
		sys.exit()
	if re.match(DiceRegex, sys.argv[2]):
		diceString = sys.argv[2]
	else:
		print("Dice Regex failed.")
		sys.exit()


# parse dice string
match = re.match(DiceRegex, diceString)
if not match:
	print("Didn't match the regex that was already checked. This shouldn't happen.")
	sys.exit()

numDice = (1 if not match.group(1) else int(match.group(1)))
diceSize = int(match.group(2))
operator = match.group(3)
operand = (0 if not match.group(4) else int(match.group(4)))
'''
print(email)
print(numDice)
print(diceSize)
print(operator)
print(operand)
'''
# Actually roll dice
diceList = []
if numDice == 0:
	print('Why are you rolling 0 dice?')
	sys.exit()
if diceSize == 0:
	print('Why are you rolling 0 sided dice?')
	sys.exit()
if operator == '/' and operand == 0:
	print('Why are you dividing by zero?')
	sys.exit()
	
for n in range(0,numDice):
	diceList.append(random.randint(1,diceSize))

diceBreakdown = ''
# format dice roll breakdown
if operator and operand:
	diceBreakdown = str(diceList) + ' ' + operator + ' ' + str(operand)
else:
	diceBreakdown = str(diceList)
	
sum = sum(diceList)
roll = 0
if operator == '+':
	roll = sum + operand
elif operator == '-':
	roll = sum - operand
elif operator == '/':
	roll = sum / operand
elif operator == '*' or operator == 'x':
	roll = sum * operand
else:
	roll = sum

print('Rolled ' + diceString + ":")
print(diceBreakdown + ' = %0.2f'%roll)

# check whether the .push20 config directory exists
# if not, create the .push20 directory as well as the config file
if not os.path.exists('./.push20'):
	print("Generating default configuration file...")
	try:
		with open('./.push20','w') as file:
			file.write('[Access]\n# Insert your API Token Here\nAPIToken=')		
	except Exception as e:
		print("Error: " + str(e))
		sys.exit()
	

	
# Create the config parser object
Config = configparser.ConfigParser()

# Attempt to load in the config file
Config.read('./.push20')
if 'Access' not in Config.sections():
	print('Something is wrong with the config file. Fix it or delete ".push20".')
	print('Looking for section Access but found ' + ', '.join(Config.sections()))
	sys.exit()

# Check if apitoken exists
if 'apitoken' not in Config.options('Access'):
	print("Couldn't find the APIToken field in the config file.")
	sys.exit()
	
	
# Check if apitoken isn't empty
APIToken = Config.get('Access','apitoken')
if not APIToken:
	print("Your API Token isn't filled in! Edit it in the .push20 file!")
	sys.exit()
	
'''
Actual Pushbullet API Section, hooray
'''

# Get information on yourself
url = 'https://api.pushbullet.com/v2/users/me'
headers = {'Access-Token': APIToken}

request = requests.get(url, headers=headers)
response = request.json()


if request.status_code != 200:
	print("Something went wrong.")
	print(str(request.status_code) + ': ' + response['error']['message'])

# send to self if no email
if not email:
	email = response['email']
	
# Set up the push creation
url = 'https://api.pushbullet.com/v2/pushes'
data = {'type': 	'note',
		'title': 	"Push20: " + diceString + ": %.2f"%roll,
		'body': 	diceBreakdown + ' = %.2f'%roll,
		'email':	email
	   }
	   
request = requests.post(url, headers=headers, data=data)
response = request.json()

if request.status_code != 200:
	print("Something went wrong.")
	print(str(request.status_code) + ': ' + response['error']['message'])

