from math import fabs
from acc.calcSpan import calcSpan

class BitfloorPctVertex(object):
	def __init__(self, queryManager, fargs, backup):
		self.queryManager = queryManager
		self.pct = .01*int(fargs['pct'])
		self.updateEvents = ['account','trade']

	def getUpdateEvents(self):
		return self.updateEvents

	def recovery(self):
		pct = self.pct
		price = self.queryManager.get_ticker()['price']
		accountQry = self.queryManager.get_account()
		usd = accountQry['balance']['usd']
		btc = accountQry['balance']['btc']
		if btc:
			vertex = (usd/pct-usd)/btc
			# if the vertex is close to the last traded price, no correcting action needed
			if fabs(price-vertex) < 0.1:
				self.update_orders()
				return
		amount = (usd-pct*usd-pct*btc*price)/price
		if amount > 0:
			self.queryManager.buy_btc(amount)
		else:
			self.queryManager.sell_btc(amount)

	def update_orders(self):
		pct = self.pct
		accountQry = self.queryManager.get_account()
		fee = 0.01*(accountQry['fee'])
		usd = accountQry['balance']['usd']
		btc = accountQry['balance']['btc']

		vertex = (usd/pct-usd)/btc
		span = calcSpan(vertex,fee)
		if (vertex%span['bid']) <= (span['bid']/2):
			vertex -= vertex%span['bid']
		else:
			vertex += span['bid'] - (vertex%span['bid'])
		span = calcSpan(vertex,fee)
		bidPrice = vertex-span['bid']
		askPrice = vertex+span['ask']

		fee = -0.001
		bidAmount = (usd-pct*usd-pct*btc*bidPrice)/bidPrice
		bidAmount -= .5*bidAmount*fee
		askAmount = fabs((usd-pct*usd-pct*btc*askPrice)/askPrice)
		askAmount -= .5*askAmount*fee

		oldOrders = self.queryManager.get_orders()
		bidId = ''
		askId = ''
		for order in oldOrders:
			if fabs(order['price']-bidPrice)<0.001:
				bidId = order['id']
			if fabs(order['price']-askPrice)<0.001:
				askId = order['id']
		if not bidId:
			bidId = self.queryManager.buy_btc(bidAmount, bidPrice)['id']
		if not askId:
			askId = self.queryManager.sell_btc(askAmount, askPrice)['id']

		idList = []
		for order in oldOrders:
			idList.append(order['id'])
		for oid in idList:
			if (oid != bidId) and (oid != askId):
				self.queryManager.cancel_order(oid)

	def backup(self):
		return {}
