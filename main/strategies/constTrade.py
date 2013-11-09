from math import fabs
from acc.calcSpan import calcSpan

class ConstTrade(object):
	def __init__(self, queryManager):
		self.queryManager = queryManager
		self.amount = 0.25
		self.vertex = 5

	def recovery(self, backup):
		vertex = 0
		if backup:
			if 'vertex' in backup.keys():
				vertex = float(backup['vertex'])
		if not vertex:
			bid = self.queryManager.get_ticker()['bid']
			ask = self.queryManager.get_ticker()['ask']
			vertex = (bid+ask)/2
			vertex -= (vertex%.01)
		self.vertex = vertex
		self.update_orders()

	def update_orders(self):
		fee = .01*self.queryManager.get_account()['fee']
		span = calcSpan(self.vertex,fee)
		bidPrice = self.vertex-span['bid']
		askPrice = self.vertex+span['ask']
		bidId = self.__getId(bidPrice)
		askId = self.__getId(askPrice)
		if not askId and not bidId:
			bidId = self.queryManager.buy_btc(self.amount, bidPrice)['id']
			askId = self.queryManager.sell_btc(self.amount, askPrice,)['id']
		elif not askId:
			self.vertex = askPrice
			span = calcSpan(self.vertex,fee)
			bidPrice = self.vertex-span['bid']
			askPrice = self.vertex+span['ask']
			bidId = self.queryManager.buy_btc(self.amount, bidPrice)['id']
			askId = self.queryManager.sell_btc(self.amount, askPrice,)['id']
		elif not bidId:
			self.vertex = bidPrice
			span = calcSpan(self.vertex,fee)
			bidPrice = self.vertex-span['bid']
			askPrice = self.vertex+span['ask']
			bidId = self.queryManager.buy_btc(self.amount, bidPrice)['id']
			askId = self.queryManager.sell_btc(self.amount, askPrice,)['id']

		orders = self.queryManager.get_orders()
		for order in orders:
			if (order['id'] != bidId) and (order['id'] != askId):
				self.queryManager.cancel_order(order['id'])

	def backup(self):
		return {'vertex':self.vertex}

	def __getId(self, price):
		orders = self.queryManager.get_orders()
		for order in orders:
			if fabs(order['price']-price) < 0.0001:
				return order['id']
		return False

