def lambda_handler(event, context):
    p = poloniex(os.environ['KEY'], os.environ['SECRET'])

    poloBalance = p.returnBalance()

    return json.loads(
        '{"version":"1.0","response":{"outputSpeech":{"type":"PlainText","text":"Your polo balance is ' + str(
            poloBalance) + ' USD. Nice! "},"shouldEndSession":true}}')


import urllib
import urllib2
import json
import hmac
import hashlib
import time
import os


class poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def api_query(self, command, req={}):

        req['command'] = command
        req['nonce'] = int(time.time() * 1000)

        post_data = urllib.urlencode(req)

        sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()

        headers = {
            'Sign': sign,
            'Key': self.APIKey
        }

        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))

        return json.loads(ret.read())

    def get_bitcoin_price_polo(self):

        ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=returnTicker'))

        payload = json.loads(ret.read())

        bitcoinPrice = payload['USDT_BTC']['last']

        bitcoinPriceFloat = float(bitcoinPrice)

        return bitcoinPriceFloat

    def returnBalance(self):

        bitcoinPrice = self.get_bitcoin_price_polo()

        balances = self.api_query('returnCompleteBalances')

        totalBtcBalance = 0

        for coin in balances:
            balancePerCoin = balances[coin]
            btcValue = float(balancePerCoin['btcValue'])
            if btcValue > 0:
                totalBtcBalance = totalBtcBalance + btcValue

        totalValueInUSD = round((totalBtcBalance * bitcoinPrice), 2)

        return str(totalValueInUSD)
