# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 08:35:37 2019

@author: TELTEL
"""
import websocket
import bFSocketWrapper
def onMsgMethod(self, ws, message):
    print(message)
    
bF = bFSocketWrapper.RealtimeAPI(url="wss://ws.lightstream.bitflyer.com/json-rpc",onMsgMethod=onMsgMethod)
bF.run()
print(3)

"""
こっちでデータ処理の関数書いてWrapperにimport
で、websocket起動、on_messageをonMsgMethodに指定

Wrapper側で受け取ったデータの処理をimportした関数、MainProcess.onMsgMethod(data)で行う
結果をクラスか何かにしてこっちで呼び出して加工して使う？

今は実際に稼働させるとmodule "bFSocketWrapper" has no attribute "RealtimeAPI"のエラーが出る

やっぱりimportしあうとエラーが出るっぽい
となるとどうやって向こうにメソッドを入れるのか分からない
abcdaみたいに片手渡しで一周させるとエラー回避できそうだけどそうじゃない
"""