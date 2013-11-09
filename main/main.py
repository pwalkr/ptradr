from common.interface import Interface

interfaceList = ['bitfloor','mtgox']
interfaces = {}

def listOpts():
	for key in options.keys():
		print key+': '+options[key][1]
	print 'Or pick an interface for more options'

def listInterfaces():
	for key in interfaces.keys():
		print '    '+key

def startInterface():
	global interfaces
	print 'Pick from:'
	for interface in interfaceList:
		if interface not in interfaces:
			print '    '+interface
	userIn = raw_input(' > ')
	if userIn in interfaceList:
		if userIn not in interfaces:
			interfaces[userIn] = Interface(userIn)
			interfaces[userIn].start()
		else:
			print userIn+' is already running.'
	else:
		print 'That is not a recognized interface.'

def stopInterface():
	global interfaces
	if interfaces:
		print 'Which interface would you like to stop?'
		for key in interfaces.keys():
			print '    '+key
		userIn = raw_input(' > ')
		if userIn in interfaces:
			interfaces[userIn].command('stop')
			interfaces.pop(userIn)
		else:
			print 'That is not a valid interface.'

def stopAll():
	global interfaces
	for interface in interfaces.keys():
		interfaces[interface].command('stop')
	interfaces = {}

options = {'help':  [listOpts,          'print this message'],
           'list':  [listInterfaces,    'list running interfaces'],
           'start': [startInterface,    'start a new interface'],
           'stop':  [stopInterface,     'stop an interface'],
           'quit':  [stopAll,           'shut down operations']}
listOpts()
userIn = ''
while userIn != 'quit':
	userIn = raw_input('--> ')

	# clean up list of running interfaces (just in case)
	dead = []
	for key in interfaces.keys():
		if not interfaces[key].status:
			dead.append(key)
	for key in dead:
		interfaces.pop(key)

	if userIn in options:
		options[userIn][0]()
	elif userIn in interfaces:
		interfaces[userIn].command('help')
		secondIn = raw_input(userIn+'> ')
		interfaces[userIn].command(secondIn)
	else:
		print 'That is not a valid command, please try again.'
