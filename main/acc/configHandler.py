from ConfigParser import SafeConfigParser

def getConf(cfgType):
	conf = {'auth':{},
	        'backup':{}}
	config = SafeConfigParser()

	config.read('conf/auth/'+cfgType+'.auth')
	for arg in config.items('auth'):
		conf['auth'][arg[0]] = arg[1]

	config.read('conf/'+cfgType+'.cfg')
	for arg in config.items('backup'):
		conf['backup'][arg[0]] = arg[1]
	return conf

def setConf(cfgType, fargs):
	config = SafeConfigParser()
	config.read('conf/'+cfgType+'.cfg')
	for key in fargs.keys():
		config.set('backup',key,str(fargs[key]))
	cfgFile = open('conf/'+cfgType+'.cfg','w')
	config.write(cfgFile)
	cfgFile.close()