# -*- coding: utf-8 -*-


import sys
import json
import websocket
import time
import bFSocketWrapper
import mexSocketWrapper
import finexSocketWrapper
import threading

bF_api = {}
mex_api = {}
finex_api = {}

"""API key secretの読み込み"""
"""
with open(r'your_api-data_path',"r") as f:
    api_data = json.loads(f)
    bF_api["key"] = api_data["bf"]["key"]
    bF_api["secret"] = api_data["bf"]["secret"]
    mex_api["key"] = api_data["mex"]["key"]
    mex_api["secret"] = api_data["mex"]["secret"]
    finex_api["key"] = api_data["finex"]["key"]
    finex_api["secret"] = api_data["finex"]["secret"]
"""
data_bF = []
data_mex = []
data_finex = []
a = 0
def onMsgMethod4bF(message):
    global data_bF
    if data_bF
    data_bF.append(message)
    data_mex.pop(0)


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
mex = bitmex_websocket.BitMEXWebsocket(endpoint=mexSocketWrapper.BitMEXWebsocket.endpoint,symbol=bitmex_websocket.BitMEXWebsocket.symbol,onMsgMethod=onMsgMethod4mex)
finex = bitfinex_websocket.RealtimeAPI(url=finexSocketWrapper.RealtimeAPI.url,onMsgMethod=onMsgMethod4finex)

"""
メインモジュールに動きがない状態で一定時間がたつと落ちるみたいなのでループを回す?

上記dictに突っ込んでると止まらないみたい
それから、変数参照するときはEventオブジェクト使うといいかも
"""
#def Allrun():
bF.run()
mex.get_instrument()
finex.run()

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
#threading.Thread(target=Allrun())
