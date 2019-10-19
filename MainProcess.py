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

"""各Wrapperから流れてきたデータのログを貯める"""
data_bF = []
data_mex = []
data_finex = []
log_count = 1000    #ログ記録量

"""各ラッパーからデータを持ってくる(成型追加するかも)メソッド"""

def onMsgMethod4bF(message):
    data_bF.append(message)
    print(len(data_bF))
    if len(data_bF) > log_count:
        data_bF.pop(0)
    if len(data_bF)%20 == 0:
        print("setsimasune")
        aaaa.set()
        #Switch.switch_set

    #print(data_bF[-1])
def onMsgMethod4mex(message):
    data_mex.append(message)
    if len(data_mex) > log_count:
        data_mex.pop(0)
    #print(data_mex[-1])
def onMsgMethod4finex(message):
    data_finex.append(message)
    if len(data_finex) > log_count:
        data_finex.pop(0)
    #print(data_finex[-1])

"""eventの処理をこっちで行いたくて、スイッチをWrapperに置きたい""
waitが欲しがってるselfがそれを包むメソッドのことなら、とりあえずこちらで
waitを含むメソッドを定義してやって向こうで呼び出してやる？

インスタンス化されてるwaitが望んでるselfはthreading.Event()のことでよかった
で、threading.Event()の入ってる変数名でどこのスレッドをwaitしてsetするか判別してるっぽい
めっちゃ便利
"""
"""
class Switch:
    def switch_wait():
        print("switch_off")
        x.threading.Event.wait()
        print("switch_on")

    def switch_set():
        threading.Event.set()
"""
def lll():
    print("hajime")
    while True:
        aaaa.wait()
        print("owari")
        aaaa.clear()
def kkk():
    print("kottihadou?")
    cccc.wait()
    print("kottimoowarunkai")
    cccc.clear()


"""websocketの呼び出し""
この時、このモジュール内で定義したメソッドを指定してやることで、ラッパー側にimportさせる必要がなくなり、
またメソッド内のデータも共有される。
ただ、共有されたデータをメソッドから出す方法はglobal化する方法しか知らない。
↑globalしなくてもよかった
"""
bF = bFSocketWrapper.RealtimeAPI(url=bFSocketWrapper.RealtimeAPI.url,onMsgMethod=onMsgMethod4bF)#ここで指定したonMethodoによる変数の移動が難しい、変数というか受信データ
mex = mexSocketWrapper.BitMEXWebsocket(endpoint=mexSocketWrapper.BitMEXWebsocket.endpoint,symbol=mexSocketWrapper.BitMEXWebsocket.symbol,onMsgMethod=onMsgMethod4mex)
finex = finexSocketWrapper.RealtimeAPI(url=finexSocketWrapper.RealtimeAPI.url,onMsgMethod=onMsgMethod4finex)


"""各websocketの稼働""
メインモジュールに動きがない状態で一定時間がたつと落ちるみたいなのでループを回す?
配列に突っ込んでると止まらないみたい
それから、変数参照するときはEventオブジェクト使うといいかも？
"""
#def Allrun():
#x = Switch()
#Switch.switch_wait()
aaaa=threading.Event()
cccc=threading.Event()
bbbb = threading.Thread(target=lll)
dddd=threading.Thread(target=kkk)
bbbb.start()
dddd.start()
print("ugoita")
bF.run()
mex.get_instrument()
finex.run()

print("wait")
time.sleep(60)
print("end")
"""データ成型の具体的な必要性、イメージがわかないのでまずこっちで全部やってみる"""
#if threading.Event.is_set("params" in data_bF):
    #print("getdata")
"""
        if threading.Event.is_set(len(data_bF[-1]["params"]["message"]) > 2):
            for i in range(0,len(data_bF[-1]["params"]["message"])):
                if data_bF[-1]["params"]["message"][i]["side"] == "BUY":
                    if data_bF[-1]["params"]["message"][i]["size"] > 1:
                        print("買います")
"""













#threading.Thread(target=Allrun())
