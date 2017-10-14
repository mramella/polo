def lambda_handler(event, context):

    p = poloniex(os.environ['KEY'], os.environ['SECRET'])
    
    poloBalance = p.returnBalance()

    return json.loads('{"version":"1.0","response":{"outputSpeech":{"type":"PlainText","text":"Your polo balance is ' + str(poloBalance) + ' USD."},"shouldEndSession":true}}')

import urllib
import json
import hmac
import hashlib
import time 
import os
import boto3
import datetime

class poloniex:

    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret
 
    def api_query(self, command, req={}):
            
            req['command'] = command
            req['nonce'] = int(time.time()*1000)
            
            post_data = urllib.parse.urlencode(req)
            post_data = post_data.encode('utf-8') # data should be bytes
 
            sign = hmac.new(bytes(self.Secret, 'latin-1'), post_data, hashlib.sha512).hexdigest()
            
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }
 
            ret = urllib.request.urlopen(urllib.request.Request('https://poloniex.com/tradingApi', post_data, headers))
            
            return json.loads(ret.read())

    def get_bitcoin_price_polo(self):
        
            ret = urllib.request.urlopen(urllib.request.Request('https://poloniex.com/public?command=returnTicker'))
            
            payload = json.loads(ret.read())
            
            bitcoinPrice = payload['USDT_BTC']['last']
            
            bitcoinPriceFloat = float(bitcoinPrice)
            
            return bitcoinPriceFloat

    def returnBalance(self):
        
        bitcoinPrice = self.get_bitcoin_price_polo()
        
        balances = self.api_query('returnCompleteBalances')

        totalBtcBalance = 0
        totalUsdtBalance = 0
        
        for coin in balances:
            balancePerCoin = balances[coin]
            if coin == 'USDT':
                totalUsdtBalance = float(balancePerCoin['available'])
            else:
                btcValue = float(balancePerCoin['btcValue'])
                if btcValue > 0:
                    totalBtcBalance = totalBtcBalance + btcValue

        totalValueInUSD = (totalBtcBalance * bitcoinPrice) + totalUsdtBalance
        
        return str(round(totalValueInUSD, 2))
 
