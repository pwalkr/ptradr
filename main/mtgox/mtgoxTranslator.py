from datetime import datetime
from mtgoxHttpInterface import MtgoxHttpInterface


class MtgoxTranslator(object):
	def __init__(self, auth):
		self.httpInterface = MtgoxHttpInterface(auth['key'],auth['secret'])
		self.orderTypes = {}

	def get_ticker(self):
		tickQry = self.httpInterface.get_ticker()
		if 'error' not in tickQry:
			ticker = {'time':datetime.today().strftime('%y-%m-%d %H:%M:%S'),
			          'price':float(tickQry['ticker']['last']),
					  'bid':float(tickQry['ticker']['buy']),
					  'ask':float(tickQry['ticker']['sell'])}
			tickQry = ticker
		return tickQry

	def get_depth(self):
		depthQry = self.httpInterface.get_depth()
		if 'error' not in depthQry:
			depth = {'time':datetime.today().strftime('%y-%m-%d %H:%M:%S'),
			         'bid':[],'ask':[]}
			for order in depthQry['asks']:
				depth['ask'].append(order)
			depthQry['bids'].reverse() # normally low to high (price)
			for order in depthQry['bids']:
				depth['bid'].append(order)
			depthQry = depth
		return depthQry

	def get_account(self):
		accountQry = self.httpInterface.get_info()
		if 'error' not in accountQry:
			balance = {'usd':float(accountQry['Wallets']['USD']['Balance']['value']),
					   'btc':float(accountQry['Wallets']['BTC']['Balance']['value'])}
			fee = float(accountQry['Trade_Fee'])
			accountQry = {'time':datetime.today().strftime('%y-%m-%d %H:%M:%S'),
			              'balance':balance,
			              'fee':fee}
		return accountQry

	def get_orders(self):
		orderQry = self.httpInterface.get_orders()
		if 'error' not in orderQry:
			self.orderTypes = {}
			orderList = []
			for order in orderQry['orders']:
				otype = 'buy' if order['type'] == 2 else 'sell'
				self.orderTypes[order['oid']] = order['type']
				orderList.append({'id':order['oid'],
								  'type':otype,
								  'amount':float(order['amount']),
								  'price':float(order['price'])})
			orderQry = orderList
		return orderQry

	def buy_btc(self,amount,price = 0):
		if amount < 0.01:
			return {'error':'Must trade at least 0.01'}
		buyQry = self.httpInterface.buy_btc(amount,price)
		if 'error' not in buyQry:
			self.orderTypes[buyQry['oid']] = 2
			order = {'id':buyQry['oid'],
					 'type':'buy',
					 'amount':amount,
					 'price':price}
			buyQry = order
		return buyQry

	def sell_btc(self,amount,price = 0):
		if amount < 0.01:
			return {'error':'Must trade at least 0.01'}
		sellQry = self.httpInterface.sell_btc(amount,price)
		if 'error' not in sellQry:
			self.orderTypes[sellQry['oid']] = 1
			order = {'id':sellQry['oid'],
					 'type':'sell',
					 'amount':amount,
					 'price':price}
			sellQry = order
		return sellQry

	def cancel_order(self,oid):
		if oid not in self.orderTypes:
			return {'error':'That is not a valid order id'}
		cancelQry = self.httpInterface.cancel_order(oid,self.orderTypes[oid])
		if 'error' not in cancelQry:
			self.orderTypes.pop(oid)
			cancelQry = {'id':oid}
		return cancelQry