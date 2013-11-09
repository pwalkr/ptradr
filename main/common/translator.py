from bitfloor.bitfloorTranslator import BitfloorTranslator
from mtgox.mtgoxTranslator import MtgoxTranslator

aliases = {'bitfloor':BitfloorTranslator,
           'mtgox':MtgoxTranslator}

class Translator(object):
	def __init__(self, interfaceType, auth):
		self.alias = aliases[interfaceType](auth)

	# {'time':string, 'price':float, 'bid':float, 'ask':float}
	def get_ticker(self):
		return self.alias.get_ticker()

	# {'time':string, 'bid':[{'price':float,'amount':float)], 'ask':[{'price':float,'amount':float)]}
	def get_depth(self):
		return self.alias.get_depth()

	# {'time':string, 'fee':float(%), 'balance':{'btc':float,'usd':float}}
	def get_account(self):
		return self.alias.get_account()

	# [{'id':str, 'type':str(buy/sell), 'amount':float, 'price':float}]
	def get_orders(self):
		return self.alias.get_orders()

	# {'id':str, 'type':str(buy/sell), 'amount':float, 'price':float}
	def buy_btc(self,amount,price = 0):
		return self.alias.buy_btc(amount, price)

	# {'id':str, 'type':str(buy/sell), 'amount':float, 'price':float}
	def sell_btc(self,amount,price = 0.01):
		return self.alias.sell_btc(amount, price)

	# {'id':str}
	def cancel_order(self,oid):
		return self.alias.cancel_order(oid)