from ConfigParser import SafeConfigParser
import random
from acc.calcSpan import calcSpan
from mtgoxTranslator import MtgoxTranslator

authFile = SafeConfigParser()
authFile.read('conf/mtgox.auth')
auth = {'key':authFile.get('auth','key'),
        'secret':authFile.get('auth','secret')}
translator = MtgoxTranslator(auth)

def cancelAll():
    orders = translator.getOrders()
    print orders
    for order in orders:
        print translator.cancelOrder(order['id'])

def printDepth():
    depth = translator.getDepth()
    for key in depth.keys():
        print key
        for order in depth[key]:
            print str(order)

def printOrders():
    orderList = translator.getOrders()
    for order in orderList:
        print order

def testSpan():
    fee = 0.006
    i = 0
    random.seed()
    passed = True
    while i < 100:
        randPrice = float(random.randrange(100,1000))/100
        span = calcSpan(randPrice, fee)
        askspan = (randPrice+span)*fee*2
        msg = '@ '+str(randPrice)+' span >'+str(askspan)+'... :'+str(span)
        print msg
        if not (span>askspan):
            passed = False
        i += 1
    print passed

print calcSpan(5.6,.006)

