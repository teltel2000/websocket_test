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
bitflyerlog = []
data_bf = {}
data_mex = {}
data_finex = {}
a = 0
def onMsgMethod4bF(message):
    global data_bF
    data_bF = message
    print(message)
def onMsgMethod4mex(message):
    global data_mex,a
    data_mex = message
    a += 1
    print(message)
def onMsgMethod4finex(message):
    global data_finex
    data_finex = message
    print(message)
bF = bFSocketWrapper.RealtimeAPI(url=bFSocketWrapper.RealtimeAPI.url,onMsgMethod4bF=onMsgMethod4bF)#ここで指定したonMethodoによる変数の移動が難しい、変数というか受信データ
mex = bitmex_websocket.BitMEXWebsocket(endpoint=bitmex_websocket.BitMEXWebsocket.endpoint,symbol=bitmex_websocket.BitMEXWebsocket.symbol,onMsgMethod4mex=onMsgMethod4mex)
finex = bitfinex_websocket.RealtimeAPI(url=bitfinex_websocket.RealtimeAPI.url,onMsgMethod4finex=onMsgMethod4finex)

bF.run()
mex.get_instrument()
finex.run()
print(a)




"""
こっちでデータ処理の関数書いてWrapperにimport     ←これにこだわる必要なくない？>>30
で、websocket起動、on_messageをonMsgMethodに指定

Wrapper側で受け取ったデータの処理をimportした関数、MainProcess.onMsgMethod(data)で行う
結果をクラスか何かにしてこっちで呼び出して加工して使う？

今は実際に稼働させるとmodule "bFSocketWrapper" has no attribute "RealtimeAPI"のエラーが出る

やっぱりimportしあうとエラーが出るっぽい
となるとどうやって向こうにメソッドを入れるのか分からない
abcdaみたいに片手渡しで一周させるとエラー回避できそうだけどそうじゃない

2019/10/17
向こうでonMsgMsgMethod定義してこっちでそれをimport、それから指定してws起動
Wrapperで受け取ったデータをWrapperで定義したonMsgMethodで～～～

>>43の方法だと"いろんな取引所のデーターを総合してシグナルとしてトレードしたいなら、ラッパー内に置くのはデーター成型くらいにして、エッジになる判定とかはメインで書いたほうが、あとあと面倒にならないです"
も問題ないし、そもそも為替さんに指摘してもらったwsをラッパーで呼び出すってことで一つのスレッドできてね？ってのも解決できる
向こうで定義してるから余計な問題も出ない

結局、向こうのon_messageに処理書くのと同じことになって地球一周してきた感が否めない
"""