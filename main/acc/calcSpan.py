def calcSpan(price, fee):
    increment = 0.01
    bidSpan = price*fee*2
    askSpan = (price+bidSpan)*fee*2
    span = {'bid':(bidSpan+increment-(bidSpan%increment)),
            'ask':(askSpan+increment-(askSpan%increment))}
    return span