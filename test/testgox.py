#!/usr/bin/python

from time import time
from base64 import b64encode,b64decode
import hmac
from hashlib import sha512
from urllib import urlencode
import urllib2
from contextlib import closing
from json import load

from ConfigParser import SafeConfigParser
from math import fabs

def Test():
	print Ticker()

conf = SafeConfigParser()
conf.read('mtgox.auth')
key = conf.get('auth','key')
secret = conf.get('auth','secret')
count = 0

def Ticker():
	return Query('data/ticker.php', auth=False)

def Info():
	return Query('info.php')

def Orders():
	return Query('getOrders.php')

def History(currencyType = 'BTC'):
	if currencyType != 'BTC' and currencyType != 'USD':
		print 'Must request BTC or USD'
	else:
		history = Query('history_'+currencyType+'.csv')
		f = open(currencyType+'_History.csv','w')
		f.write(history)
		f.close()

def Buy(amt, price=0):
	data = {u'amount':amt}
	if price != 0:	
		data[u'price'] = price
	return Query('buyBTC.php',data)

def Sell(amt, price=0):
	data = {u'amount':amt}
	if price != 0:
		data[u'price'] = price
	return Query('sellBTC.php',data)

def Query(path,post_data = {},auth = True):
		if auth:
			global count
			post_data['nonce'] = int(time()*1000000) + count
			count += 1
			post_data = urlencode(post_data)
			signed = b64encode(str(hmac.new(
				b64decode(secret),
				post_data,
				sha512).digest()))
			headers = ({
				'User_Agent':'goxbot',
				'Rest_Key':key,
				'Rest_Sign':signed})
		else:
			post_data = {}
			headers = {}
		url = 'https://mtgox.com/api/0/'+path
		req = urllib2.Request(url,post_data,headers)
		with closing(urllib2.urlopen(req)) as res:
			if path.endswith('php'):
				data = load(res)
			else:
				data = res.read()
		return data

Test()
