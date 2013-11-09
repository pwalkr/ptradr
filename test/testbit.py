#!/usr/bin/python
from ConfigParser import SafeConfigParser
import urllib2

from bitfloorHttpInterface import BitfloorHttpInterface

def Test():
	print account()

conf = SafeConfigParser()
conf.read('bitfloor.auth')
key = conf.get('auth','key')
secret = conf.get('auth','secret')
interface = BitfloorHttpInterface(key,secret)
count = 0

def ticker():
	return interface.get_tick()

def depth():
	return interface.get_book(2)

def account():
	return interface.get_account()

def orders():
	return interface.get_orders()

def buy(amount, price = 0):
	return interface.set_order(amount,price,0)

def sell(amount, price = 0.01):
	return interface.set_order(amount,price,1)

Test()
