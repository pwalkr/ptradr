from threading import Thread
from time import sleep
from acc.error import BadQuery

class DataMiner(Thread):
	def __init__(self, queryManager, eventHandler):
		Thread.__init__(self)
		self.queryManager = queryManager
		self.eventHandler = eventHandler
		self.updateIndex = 0
		self.tickRate = 30

	def run(self):
		self.listening = True
		while self.listening:
			self.updateIndex += 1
			if self.listening:
				try:
					ordersUpdated = False
					tickerUpdated = self.queryManager.update_ticker()
					if tickerUpdated:
						ordersUpdated = self.queryManager.update_orders()
					if ordersUpdated:
						self.updateIndex = 0
						self.queryManager.update_account()
						self.eventHandler.handle('update')
				except BadQuery:
					self.listening = False
					self.eventHandler.handle('error')
				else:
					sleep(self.tickRate/2)

			if self.listening:
				if self.updateIndex >= 20:
					self.updateIndex = 0
					try:
						self.queryManager.update_account()
						self.queryManager.update_orders()
					except BadQuery:
						self.listening = False
						self.eventHandler.handle('error')
					else:
						self.eventHandler.handle('update')

				sleep(self.tickRate/2)

	def stop(self):
		self.listening = False
