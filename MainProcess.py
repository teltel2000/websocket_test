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
def round1000(num):
    num = int(num)
    if int(str(num)[-3])>4:
        num += 1000
    for i in range(-3,0):
        while str(num)[i] != "0":
            num -= 1
    return num


"""各Wrapperから流れてきたデータのログを貯める"""
"""
full 生データまんま
price 価格
size ロングを正、ショートを負とした瞬間出来高
absize 絶対値のsize
"""
data_bF = {"exe":{"full":[],"price":[],"size":[],"absize":[]},"board":[]}
data_mex = []
data_finex = []
log_count = 1000    #ログ記録量
vpp = {"size":[],"absize":[]} #5min volume per price

"""各ラッパーからデータを持ってくる(成型追加するかも)メソッド"""

def onMsgMethod4bF(message):
    """exectionの成型"""
    """full price sizeに分けて、sizeはショートの場合マイナス化"""
    number = len(message["params"]["message"])
    if "lightning_executions_FX_BTC_JPY" in message["params"].values():
        data_bF["exe"]["full"].append(message)
        for i in range(0,number):
            data_bF["exe"]["price"].append(message["params"]["message"][i]["price"])
            data_bF["exe"]["absize"].append(message["params"]["message"][i]["size"])
        if message["params"]["message"][-1]["side"] == "SELL":
            data_bF["exe"]["full"][-1]["params"]["message"][-1]["size"] *= -1
        for i in range(0,number):
            data_bF["exe"]["size"].append(data_bF["exe"]["full"][-1]["params"]["message"][-1]["size"])
        #print(str(data_bF["exe"]["price"][-1])+"____"+str(data_bF["exe"]["size"][-1]))

        """↓とりあえず置いてるだけ"""
        #print("executionsを発見しました")
        bF_exe_ev.set()
        print(len(data_bF["exe"]["price"]))
    elif len(data_bF["exe"]["price"])>1000:
        vppdictsize = {}
        vppdictabsize = {}
        lastrap = {}
        lastrapab = {}
        pricelist = []
        vppnum = len(data_bF["exe"]["price"])
        print("test")
        print("vppnum")
        for i in range(0,vppnum):

            pricelist.append(round1000(data_bF["exe"]["price"][i]))
            print(len(pricelist))
            if pricelist[i] in vppdictsize:
                vppdictsize[pricelist[i]] += data_bF["exe"]["size"][i]

                vppdictabsize[pricelist[i]] += data_bF["exe"]["absize"][i]
                print("vppdictabsize")
            else:
                vppdictsize[pricelist[i]] = data_bF["exe"]["size"][i]
                vppdictabsize[pricelist[i]] = data_bF["exe"]["absize"][i]
            #print(vppdictsize)
            #print(vppdictabsize)
        lastrap[time.time()] = vppdictsize
        lastrapab[time.time()] = vppdictabsize
        vpp["size"].append(lastrap)
        vpp["absize"].append(lastrapab)
        data_bF["exe"]["price"].clear()
        data_bF["exe"]["size"].clear()
        print(vpp)
        if len(vpp["size"]) > 3000:
            vpp["size"].pop(0)
            vpp["absize"].pop(0)

        """boardの成型"""
    elif "lightning_board_FX_BTC_JPY" in message["params"].values():
        data_bF["board"].append(message)
        #print(message)
    #print(len(data_bF))

    """logはとりあえず1000程貯める(全然少ない)"""
    if len(data_bF["exe"]["full"]) > log_count:
        data_bF["exe"]["full"].pop(0)
    elif len(data_bF["board"]) > log_count:
        data_bF["board"].pop(0)


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

"""eventの処理をこっちで行いたくて、スイッチをWrapperに置きたい"""
"""
変数は絶え間なく更新されているので整理せずに条件分けに突っ込むと途中で変わって紛れ込む
"""
"""
ってか以下のデータ成型はイベントスレッド内で行う必要ないな
"""
def bF_exe_f():
    print("bitFlyer_lightning_executions")
    while True:
        bF_exe_ev.wait()
        time.sleep(30)
        bF_exe_ev.clear()
runev = threading.Event()
def runevent():
    runev.set()
"""websocketの呼び出し"""
bF = bFSocketWrapper.RealtimeAPI(url=bFSocketWrapper.RealtimeAPI.url,onMsgMethod=onMsgMethod4bF,runevent = runevent)#ここで指定したonMethodoによる変数の移動が難しい、変数というか受信データ
mex = mexSocketWrapper.BitMEXWebsocket(endpoint=mexSocketWrapper.BitMEXWebsocket.endpoint,symbol=mexSocketWrapper.BitMEXWebsocket.symbol,onMsgMethod=onMsgMethod4mex,runevent = runevent)
finex = finexSocketWrapper.RealtimeAPI(url=finexSocketWrapper.RealtimeAPI.url,onMsgMethod=onMsgMethod4finex,runevent = runevent)


"""
メインモジュールに動きがない状態で一定時間がたつと落ちるみたいなのでループを回す?
配列に突っ込んでると止まらないみたい
それから、変数参照するときはEventオブジェクト使うといいかも？
"""
bF_exe_ev=threading.Event()
bF_exe_th1=threading.Thread(target=bF_exe_f)
bF_exe_th1.start()


"""websocketの稼働""
接続が途切れた後に自動で再接続する"""
def Allrun():
    runswitch = {"bf":False,"mex":False,"finex":False}
    while True:
        print(1)
        runev.wait()
        print(2)
        if not runswitch["bf"]:
            runswitch["bf"]=bF.run()
        if not runswitch["mex"]:
            runswitch["mex"]=mex.get_instrument()
        if not runswitch["finex"]:
            runswitch["finex"]=finex.run()
        runevent.clear()
allrun = threading.Thread(target=Allrun)
allrun.start()
runev.set()

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
