# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 08:35:37 2019

@author: TELTEL
"""
import websocket
import time
import bFSocketWrapper
import bitmex_websocket
import bitfinex_websocket
import threading
data_bF = []
data_mex = []
data_finex = []
a = 0
def onMsgMethod4bF(message):
    global data_bF
    data_bF.append(message)
    """
    if len(data_bF) > 1000:
        data_bF.pop(0)
    if threading.Event.is_set("params" in data_bF):
        if threading.Event.is_set(len(data_bF[-1]["params"]["message"]) > 2):
            for i in range(0,len(data_bF[-1]["params"]["message"])):
                if data_bF[-1]["params"]["message"][i]["side"] == "BUY":
                    if data_bF[-1]["params"]["message"][i]["size"] > 1:
                        print("買います")
     """               
    
    #print(message)
def onMsgMethod4mex(message):
    global data_mex
    data_mex.append(message)
    if len(data_mex) > 1000:
        data_mex.pop(0)
    #print(message)
def onMsgMethod4finex(message):
    global data_finex
    data_finex.append(message)
    if len(data_finex) > 1000:
        data_finex.pop(0)
    #print(message)
bF = bFSocketWrapper.RealtimeAPI(url=bFSocketWrapper.RealtimeAPI.url,onMsgMethod=onMsgMethod4bF)#ここで指定したonMethodoによる変数の移動が難しい、変数というか受信データ
mex = bitmex_websocket.BitMEXWebsocket(endpoint=bitmex_websocket.BitMEXWebsocket.endpoint,symbol=bitmex_websocket.BitMEXWebsocket.symbol,onMsgMethod=onMsgMethod4mex)
finex = bitfinex_websocket.RealtimeAPI(url=bitfinex_websocket.RealtimeAPI.url,onMsgMethod=onMsgMethod4finex)

"""
メインモジュールに動きがない状態で一定時間がたつと落ちるみたいなのでループを回す?

上記dictに突っ込んでると止まらないみたい
それから、変数参照するときはEventオブジェクト使うといいかも
"""
#def Allrun():
bF.run()
mex.get_instrument()
finex.run()


#threading.Thread(target=Allrun())