"��Looper"  
#単純な売買を繰り返すシンプルなボット

実装したい機能　2019/10/14
bitfinex bitmex bitflyer現物　等の主要取引所での成り行き売買や大きな板の情報をinagoflyerの様に内部処理したい  
ポジションが偏りすぎないように満遍なく指値を置きたい  
bitflyerはポジションから順に約定処理してしまうので常に約定しなかったポジションのログを取っておきたい  
上記を利用してスワップを回避したい  
利益はbtcに変えて証拠金に追加する  
60%の下落に耐える  
ボラティリティや勢いを見て約定までの値幅を調整したり指値を深くしたりしたい  
定期的にラインに通知若しくはtwitterに報告を上げたい  
_________________________________________________________________________
2019/10/15  
ドンちゃんボットの仕組みを利用して最高値更新中は利確しない  
_________________________________________________________________________
2019/10/18  
アビトラ、乖離収束等考える  
買い専門にしたほうがいい？  
