from threading import Thread
from acc.configHandler import getConf, setConf
from acc.dataMiner import DataMiner
from acc.error import BadQuery
from common.strategy import Strategy
from data.queryManager import QueryManager

class Interface(Thread):
	def __init__(self, interfaceType):
		Thread.__init__(self)
		self.type = interfaceType
		conf = getConf(interfaceType)
		self.queryManager = QueryManager(interfaceType, conf['auth'])
		self.dataMiner = DataMiner(self.queryManager, self)
		self.strategy = Strategy(interfaceType, self.queryManager)
		self.status = False

	def status(self):
		return self.status

	def run(self):
		try:
			self.status = True
			self.queryManager.update_all()
			self.strategy.recovery(getConf(self.type)['backup'])
		except BadQuery:
			self.stop()
		else:
			self.dataMiner.start()

	def handle(self,eventType):
		if eventType == 'error':
			self.stop()
		else:
			try:
				self.strategy.update_orders()
			except BadQuery:
				self.stop()

	def stop(self):
		self.status = False
		fargs = self.strategy.backup()
		if fargs:
			setConf(self.type,fargs)
		self.dataMiner.stop()
		self.queryManager.close()

	def command(self, input):
		if input == 'help':
			print 'Options: help, balance, orders, stop'
		elif input == 'balance':
			try:
				print str(self.queryManager.update_account(force = True)['balance'])
			except BadQuery:
				print 'Something went wrong, please try again'
		elif input == 'orders':
			try:
				orders = self.queryManager.update_orders(force = True)
			except BadQuery:
				print 'Something went wrong, please try again'
			else:
				for order in orders:
					print order['type']+' '+str(order['amount'])+' at '+str(order['price'])
		elif input == 'stop':
			self.stop()
		else:
			print 'That is not a valid command'