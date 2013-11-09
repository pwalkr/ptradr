from math import fabs
from acc.error import BadQuery
from common.translator import Translator
from data.flatFileHandler import FlatFileHandler

class QueryManager(object):
	def __init__(self, interfaceType, auth):
		self.translator = Translator(interfaceType, auth)
		self.dataHandler = FlatFileHandler(interfaceType)

	def update_all(self):
		tickerQry = self.translator.get_ticker()
		accountQry = self.translator.get_account()
		orderQry = self.translator.get_orders()
		if ('error' not in tickerQry) and \
				('error' not in accountQry) and \
				('error' not in orderQry):
			self.ticker = tickerQry
			self.account = accountQry
			self.orders = orderQry
		else:
			raise BadQuery

	def update_ticker(self, force = False):
		tickerQry = self.translator.get_ticker()
		if 'error' not in tickerQry:
			if not self.ticker:
				self.ticker = tickerQry
				return tickerQry
			if force \
					or (fabs(self.ticker['price']-tickerQry['price'])>.001) \
					or (fabs(self.ticker['bid']-tickerQry['bid'])>.001) \
					or (fabs(self.ticker['ask']-tickerQry['ask'])>.001):
				if not force:
					self.dataHandler.set_ticker(tickerQry)
					self.ticker = tickerQry
				return tickerQry
			return False
		else:
			raise BadQuery

	def update_account(self, force = False):
		accountQry = self.translator.get_account()
		if 'error' not in accountQry:
			if force \
				    or (fabs(self.account['balance']['btc']-accountQry['balance']['btc'])>.001) \
					or (fabs(self.account['balance']['btc']-accountQry['balance']['btc'])>.001):
				if not force:
					self.dataHandler.set_account(accountQry)
					self.account = accountQry
				return accountQry
			return False
		else:
			raise BadQuery

	def update_orders(self, force = False):
		orderQry = self.translator.get_orders()
		if 'error' not in orderQry:
			if not self.orders:
				self.orders = orderQry
				return orderQry
			tradeHappened = False
			for oldOrder in self.orders:
				tradeHappened = True
				for newOrder in orderQry:
					if oldOrder['id'] == newOrder['id']:
						tradeHappened = False
						break
				if tradeHappened:
					break
			if force or tradeHappened:
				self.orders = orderQry
				return orderQry
			return False
		else:
			raise BadQuery

	def get_ticker(self):
		return self.ticker

	def get_account(self):
		return self.account

	def get_orders(self):
		return self.orders

	def buy_btc(self, amount, price = 0):
		newOrder = self.translator.buy_btc(amount, price)
		if 'error' not in newOrder:
			self.orders.append(newOrder)
			return newOrder
		raise BadQuery

	def sell_btc(self, amount, price = 0):
		newOrder = self.translator.sell_btc(amount, price)
		if 'error' not in newOrder:
			self.orders.append(newOrder)
			return newOrder
		raise BadQuery


	def cancel_order(self, oid):
		cancelQry = self.translator.cancel_order(oid)
		if 'error' not in cancelQry:
			orderIndex = -1
			for order in self.orders:
				if order['id'] == oid:
					orderIndex = self.orders.index(order)
					break
			self.orders.pop(orderIndex)
		return cancelQry

	def close(self):
		self.dataHandler.close()