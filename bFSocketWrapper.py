# -*- coding: utf-8 -*-
import requests
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
    def __init__(self, url, onMsgMethod):
        self.url = url
        self.onMsgMethod = onMsgMethod
        self.rerun_flag = "OFF"
        self.restart = 1
        #Define Websocket
        self.ws = websocket.WebSocketApp(self.url,header=None,on_open=self.on_open, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        websocket.enableTrace(True)
    def run(self):
        #ws has loop. To break this press ctrl + c to occur Keyboard Interruption Exception.
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
                self.exit()
                #self.reconnect()
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
        print(error)
        print("reconnect")
        if not self.ws.sock:
            self.reconnect()
    # when websocket closed.
    def on_close(self, ws):
        logger.info('disconnected streaming server')
        print("reconnect")
        if not self.ws.sock:
            self.reconnect()
    # when websocket opened.
    def on_open(self, ws):
        print('connected streaming server')
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
    def reconnect(self,**kwargs):
       # if not self.ws.sock:
        print(self.ws.sock)
        #print(self.ws.sock.connected)
        if self.ws.sock:
            self.ws.sock.close(**kwargs)
        print(self.ws.sock)
        if self.restart < 5:
            self.restart += 1
        print(self.restart)
        time.sleep(self.restart)
        #self.ws.sock = None
        self.run()


    url = 'wss://ws.lightstream.bitflyer.com/json-rpc'
    channel = 'lightning_executions_FX_BTC_JPY'
    channel2 = "lightning_board_FX_BTC_JPY"
