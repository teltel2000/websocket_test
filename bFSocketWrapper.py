# -*- coding: utf-8 -*-

import threading
import json
import time
import websocket
from time import sleep
from logging import getLogger,INFO,StreamHandler
#import MainProcess
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
#初期設定
data_bF = []

#API認証

"""
This program calls Bitflyer real time API JSON-RPC2.0 over Websocket
"""
class RealtimeAPI(object):
    def __init__(self, url, onMsgMethod,runevent):
        self.url = url
        self.onMsgMethod = onMsgMethod
        self.rerun_flag = "OFF"
        self.runevent = runevent
        #Define Websocket
        self.ws = websocket.WebSocketApp(self.url,header=None,on_open=self.on_open, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        websocket.enableTrace(True)
    def run(self):
        #ws has loop. To break this press ctrl + c to occur Keyboard Interruption Exception.
        while True:
            if self.rerun_flag == "OFF":
                self.wst = threading.Thread(target=lambda: self.ws.run_forever())
                self.wst.daemon = True
                self.wst.start()
                logger.debug("Started thread")
                self.rerun_flag = "ON"
            # Wait for connect before continuing
            conn_timeout = 30
            while not self.ws.sock or not self.ws.sock.connected and conn_timeout:
                sleep(1)
                conn_timeout -= 1
            if not conn_timeout:
                self.logger.error("Couldn't connect to WS! Exiting.")
                #self.exit()
                self.rerun_flag = "OFF"
                #raise websocket.WebSocketTimeoutException('Couldn\'t connect to WS! Exiting.')



            #logger.info('Web Socket process ended.')
            time.sleep(5)
    """
    Below are callback functions of websocket.
    """
    # when we get message
    def on_message(self, ws, message):

        self.data = json.loads(message)#websocket受信イベント
        self.onMsgMethod(self.data)
        #logger.info(output)

    # when error occurs
    def on_error(self, ws, error):
        logger.error(error)

    # when websocket closed.
    def on_close(self, ws):
        logger.info('disconnected streaming server')
    # when websocket opened.
    def on_open(self, ws):
        logger.info('connected streaming server')
        output_json = json.dumps(
            {'method' : 'subscribe',
            'params' : {'channel' : self.channel}
            }
        )
        output_json2 = json.dumps(
            {'method' : 'subscribe',
            'params' : {'channel' : self.channel2}
            }
        )

        ws.send(output_json)
        ws.send(output_json2)

    url = 'wss://ws.lightstream.bitflyer.com/json-rpc'
    channel = 'lightning_executions_FX_BTC_JPY'
    channel2 = "lightning_board_FX_BTC_JPY"
