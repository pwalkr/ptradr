from strategies.bitfloorPctVertex import BitfloorPctVertex
from strategies.constTrade import ConstTrade
from strategies.pctVertex import PctVertex

aliases = {'bitfloor':BitfloorPctVertex,
           'mtgox':PctVertex}

class Strategy(object):
	def __init__(self, interfaceType, queryManager):
		self.alias = aliases[interfaceType](queryManager)

	def events(self):
		return self.alias.events()

	def recovery(self, backup):
		return self.alias.recovery(backup)

	def update_orders(self):
		return self.alias.update_orders()

	def backup(self):
		return self.alias.backup()


