# memo  

実装したい機能  
2019/10/14  
bitfinex bitmex bitflyer現物 等の主要取引所での成り行き売買や大きな板の情報をinagoflyerの様に内部処理したい  
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
_________________________________________________________________________
2019/10/19  
### 具体案  
まずポジションや指値の有無、jsonファイルの記録等、注文状況の確認  
証拠金を呼び出して60％の下落を想定して仮想的に指値(ポジション取得の場合のみ)を置く  
レバレッジ4倍  
pc内では仮想的に指値を置くが、実際には現在価格から3%下までに置く  
ここから下落するたびに3%範囲に実際の指値を追加していく  
また、髭キャッチでポジションを取得、利確のための指値も置く  
イメージとしては最大リスク率60%の間で6(n)分割して一区画の間に髭キャッチの指値(ポジション取得)は二本しか置けないようにする  
つまり証拠金全部で1.8枚まで持てるとすると一区画0.01*28枚を均等に(可変だが)散らす残りの2枚を髭キャッチ用にして現在価格に追尾させる  
枚数比は適当なので再考の余地あり  
で、各取引所からの情報をもとに利確幅や指値の密度を変えていこうと思う  
ただ、上記の設定の場合10万毎に0.3枚消費するというのは変わらない  
あくまで区画は超えないようにする  
_________________________________________________________________________
2019/10/20  
oi考えたい  
記録は全てパソコンに入れておきたい、仮に1000ポジションの管理をするとしても辞書に入れるだけだし多分いける  
利益が出たらそれで現物を買って証拠金に加えたい  
日付が変わるなどswap締め切りを回避したい  
価格帯毎の時間別出来高が欲しい
