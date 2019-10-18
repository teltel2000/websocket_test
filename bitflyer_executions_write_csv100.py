# -*- coding: utf-8 -*-


import requests
import csv
import json
import time
import threading

import websocket
from time import sleep
from logging import getLogger,INFO,StreamHandler
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

"""
This program calls Bitflyer real time API JSON-RPC2.0 over Websocket
"""
class RealtimeAPI(object):

    def __init__(self, url, channel, channel2):
        self.url = url
        self.channel = channel
        self.channel2 = channel2

        #Define Websocket
        self.ws = websocket.WebSocketApp(self.url,header=None,on_open=self.on_open, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        websocket.enableTrace(True)

    def run(self):
        #ws has loop. To break this press ctrl + c to occur Keyboard Interruption Exception.
        self.ws.run_forever()
        logger.info('Web Socket process ended.')
        recconect_switch = 1
        time.sleep(5)
        return recconect_switch
    """
    Below are callback functions of websocket.
    """
    # when we get message
    def on_message(self, ws, message):
        x = 0
        output = json.loads(message)
        logger.info(output)
        if output["params"]["channel"] == "lightning_executions_FX_BTC_JPY":
            hours = int(output["params"]["message"][0]["exec_date"][11]+output["params"]["message"][0]["exec_date"][12])
            days = int(output["params"]["message"][0]["exec_date"][8]+output["params"]["message"][0]["exec_date"][9])
            months = int(output["params"]["message"][0]["exec_date"][5]+output["params"]["message"][0]["exec_date"][6])
            years = int(output["params"]["message"][0]["exec_date"][0]+output["params"]["message"][0]["exec_date"][1]+output["params"]["message"][0]["exec_date"][0]+output["params"]["message"][0]["exec_date"][2]+output["params"]["message"][0]["exec_date"][0]+output["params"]["message"][0]["exec_date"][3])
            if hours < 4:
                y = 1
            elif hours >= 4 and hours < 8:
                y = 2
            elif hours >= 8 and hours < 12:
                y = 3
            elif hours >= 12 and hours < 16:
                y = 4
            elif hours >= 16 and hours < 20:
                y = 5
            elif hours >= 20 and hours < 24:
                y = 6
            number = len(output["params"]["message"])
            x = str(years)+"_" + str(months)+"_" + str(days)+"_" + str(y)

            with open("C:\\Users\\"+x+".csv", "a") as f :
                writer = csv.writer(f,lineterminator="\n")
                for i in range(0,number):
                    writer.writerow((time.clock(),
                                output["params"]["message"][i]["id"],
                                output["params"]["message"][i]["exec_date"],
                                output["params"]["message"][i]["side"],
                                output["params"]["message"][i]["price"],
                                output["params"]["message"][i]["size"],
                                output["params"]["message"][i]["buy_child_order_acceptance_id"],
                                output["params"]["message"][i]["sell_child_order_acceptance_id"])

                                )

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

if __name__ == '__main__':
    #API endpoint
    url = 'wss://ws.lightstream.bitflyer.com/json-rpc'
    channel = 'lightning_executions_FX_BTC_JPY'
    channel2 = "lightning_board_FX_BTC_JPY"
    json_rpc = RealtimeAPI(url=url, channel=channel, channel2=channel2)
    recconect_switch = 0
    #ctrl + cで終了
    #ここからスレッドで分けたい　並列処理したい
    #スレッド処理は必要なかった　onopenに欲しいURL突っ込んでsendで送るだけ　initにchannelは入れとかないといけない
    #thread_1 = threading.Thread(target=SideWsBfboard())
    recconect_switch = json_rpc.run()
    while recconect_switch == 1:
        if recconect_switch == 1:
            recconect_switch = 0
            print("再接続します")
            recconect_switch = json_rpc.run()
