# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 08:35:37 2019

@author: TELTEL
"""
import websocket
import bFSocketWrapper
output = {}
output = bFSocketWrapper.BFWS.recent_trades()
def onMsgMethod(output):
    print(output)
bFjson_rpc = websocket.WebSocketApp(url="wss://ws.lightstream.bitflyer.com/json-rpc",header=None,on_open=bFSocketWrapper.BFWS.on_open, on_message=onMsgMethod(output), on_error=bFSocketWrapper.BFWS.on_error, on_close=bFSocketWrapper.BFWS.on_close)
    
    