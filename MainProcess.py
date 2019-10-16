# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 08:35:37 2019

@author: TELTEL
"""
import websocket
import bFSocketWrapper


    
bF = bFSocketWrapper.RealtimeAPI(url="wss://ws.lightstream.bitflyer.com/json-rpc",onMsgMethod=bFSocketWrapper.onMsgMethod)
bF.run()
while True:
    print(1)

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

>>30の方法だと"いろんな取引所のデーターを総合してシグナルとしてトレードしたいなら、ラッパー内に置くのはデーター成型くらいにして、エッジになる判定とかはメインで書いたほうが、あとあと面倒にならないです"
も問題ないし、そもそも為替さんに指摘してもらったwsをラッパーで呼び出すってことで一つのスレッドできてね？ってのも解決できる
向こうで定義してるから余計な問題も出ない
"""