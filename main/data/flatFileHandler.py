from contextlib import closing
import os.path

class FlatFileHandler(object):
	def __init__(self, interfaceType):
		self.iType = interfaceType
		self.tFile = 'log/ticker_'+interfaceType
		self.dFile = 'log/depth_'+interfaceType
		self.aFile = 'log/account_'+interfaceType
		self.cacheSize = 50
		self.ticker = []
		self.depth =[]
		self.orders = []
		if not os.path.isfile(self.tFile):
			with closing(open(self.tFile, 'w')) as fileHandle:
				fileHandle.write('time,price,bid,ask\n')
		if not os.path.isfile(self.aFile):
			with closing(open(self.aFile,'w')) as fileHandle:
				fileHandle.write('time,btc,usd\n')
#		with closing(open('log/'+self.iType+'_ticker','r')) as fileHandle:
#			for line in reversed(fileHandle.readlines()):
#				self.ticker.append(json.loads(line.rstrip()))
#				if len(self.ticker) >= (self.cacheSize/2):
#					break

	def get_ticker(self, entries):
#		if entries:
#			ticker = []
#			for entry in self.ticker:
#				ticker.append(entry)
#				if len(ticker) >= entries:
#					break
#		else:
#			ticker = self.ticker[0]
		return self.ticker

	def get_depth(self, entries):
#		if entries:
#			depth = []
#			for entry in self.depth:
#				depth.append(entry)
#				if len(depth) >= entries:
#					break
#		else:
#			depth = self.depth[0]
		return self.depth

	def get_account(self):
		return self.account

	def get_orders(self):
		return self.orders

	def set_ticker(self, ticker):
#		self.ticker.insert(0,ticker)
		csvLine = ticker['time']+       ','+ \
		          str(ticker['price'])+ ','+ \
		          str(ticker['bid'])+   ','+ \
		          str(ticker['ask'])+   '\n'
		with closing(open(self.tFile,'a')) as fileHandle:
			fileHandle.write(csvLine)
		self.ticker = ticker

	def set_depth(self, depth):
		# only write differences to log
#		self.depth.insert(0,depth)
#		bIndex = 0
#		aIndex = 0
#		with closing(open(self.dbFile, 'a')) as fileHandle:
#			fileHandle.write('price,amount,'+depth['time']+'\n')
#			for entry in depth['bid']:
#				bIndex+=1
#				fileHandle.write(str(entry[0])+',')
#				fileHandle.write(str(entry[1])+'\n')
#				if bIndex >= 20:
#					break
#			while bIndex < 20:
#				bIndex += 1
#				fileHandle.write('0,0\n')
#		with closing(open(self.daFile, 'a')) as fileHandle:
#			fileHandle.write('price,amount,'+depth['time']+'\n')
#			for entry in depth['ask']:
#				aIndex+=1
#				fileHandle.write(str(entry[0])+',')
#				fileHandle.write(str(entry[1])+'\n')
#				if aIndex >= 20:
#					break
#			while aIndex < 20:
#				aIndex += 1
#				fileHandle.write('0,0\n')
		self.depth = depth

	def set_account(self, account):
		csvLine = account['time']+      ','+\
		          str(account['balance']['btc'])+  ','+\
		          str(account['balance']['usd'])+  '\n'
		with closing(open(self.aFile,'a')) as fileHandle:
			fileHandle.write(csvLine)
		self.account = account

	def set_orders(self, orders):
		self.orders = orders

	def close(self):
#		with closing(open('log/'+self.iType+'_ticker','a')) as fileHandle:
#			for entry in reversed(self.ticker):
#				fileHandle.write(str(entry))
#		with closing(open('log/'+self.iType+'_depth','a')) as fileHandle:
#			for entry in reversed(self.depth):
#				fileHandle.write(str(entry))
		pass
