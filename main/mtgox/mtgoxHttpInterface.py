import httplib
import time
from datetime import datetime
from base64 import b64encode,b64decode
import hmac
from hashlib import sha512
from urllib import urlencode
import urllib2
import json

class MtgoxHttpInterface(object):
	def __init__(self, key, secret):
		self.key = key
		self.secret = secret
		self.count = 0
		self.timeOut = 30
		self.refreshRate = 3

	def __query(self,path,data,auth = True):
		jsonData = {}
		attempts = 1
		while attempts <= self.timeOut/self.refreshRate:
			if auth:
				data['nonce'] = int(time.time()*1000000)+self.count
				self.count += 1
				post_data = urlencode(data)
				signature = b64encode(str(hmac.new(
						b64decode(self.secret),
						post_data,
						sha512).digest()))
				headers = ({'User_Agent':'tradr',
							'Rest_Key':self.key,
							'Rest_Sign':signature})
			else:
				post_data = urlencode(data)
				headers = {}
			url = 'https://mtgox.com/api/0/'+path
			req = urllib2.Request(url,post_data,headers)

			try:
				res = urllib2.urlopen(req)
			except urllib2.URLError:
				pass
			except httplib.BadStatusLine:
				pass
			else:
				if path.endswith('csv'):
					return res.read()
				else:
					try:
						jsonData = json.load(res)
					except ValueError:
						pass
					except 'error' in jsonData:
						pass
					else:
						return jsonData
			attempts += 1
			time.sleep(self.refreshRate)
		if jsonData:
			self.__log('bad response: '+str(jsonData['error']))
		else:
			self.__log('connection timed out')
		return {'error':'something went horribly wrong'}

	def get_ticker(self):
		attempts = 1
		tickerQry = {}
		while attempts <= 5:
			tickerQry = self.__query('data/ticker.php', {}, auth=False)
			if 'error' not in tickerQry:
				return tickerQry
			attempts += 1
			time.sleep(2)
		self.__log('Bad Ticker Response:'+tickerQry['error'])
		return tickerQry

	def get_depth(self):
		return self.__query('data/getDepth.php?Currency=USD', {}, auth=False)

	def get_info(self):
		return self.__query('info.php', {})

	def get_orders(self):
		return self.__query('getOrders.php', {})

	def get_history(self,cType):
		if cType == 'BTC' or cType == 'USD':
			return self.__query('history_'+cType+'.csv', {})

	def buy_btc(self, amt, price = 0):
		if not price:
			data = {'amount':amt}
		else:
			data = {'amount':amt,'price':price}
		buyQry = self.__query('buyBTC.php',data)
		if 'error' not in buyQry:
			msg = 'buy: '+str(amt)+' at '+str(price)+' '+buyQry['oid']
			self.__log(msg)
		return buyQry

	def sell_btc(self, amt, price = 0):
		if not price:
			data = {'amount':amt}
		else:
			data = {'amount':amt,'price':price}
		sellQry = self.__query('sellBTC.php',data)
		if 'error' not in sellQry:
			msg = 'sell: '+str(amt)+' at '+str(price)+' '+sellQry['oid']
			self.__log(msg)
		return sellQry

	def cancel_order(self, oid, otype):
#        oType = 'Sell' if order['type'] == '1' else 'Buy'
		data = {'oid':oid,'type':otype}
		cancelQry = self.__query('cancelOrder.php',data)
		if 'error' not in cancelQry:
			msg = 'cancel: '+oid
			self.__log(msg)
		return cancelQry

	def __log(self, message):
		tStamp = datetime.today().strftime('%y-%m-%d %H:%M:%S')
		logMsg = tStamp+' '+str(message)
		f = open('log/mtgox.log', 'a')
		f.write(logMsg+'\n')
		f.close()
