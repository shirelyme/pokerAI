#! /usr/bin/env python
# -*- coding:utf-8 -*-
import time
import datetime
import json
from websocket import create_connection
import sys
import pokeCardJudge
import logging
import os
import traceback
import search

# pip install websocket-client
ws = None
myhandPoker=None
players = []
players_data_deal = []
players_data_flop = []
players_data_turn = []
players_data_river =[]
chips=1000
total_bet=0
players_action = []

game_status = 0

table_board=[]

debug_maping ={
    #    module_4 debug level => python #logging degbug level
    'error':logging.ERROR,
    'info':logging.INFO,
    'warning':logging.WARNING,
    'debug':logging.DEBUG,
}
def init_logger():
    logger = logging.getLogger()
    formatter_str = '[%(asctime)s]_[%(levelname)s]_[%(filename)s:%(lineno)d]_[%(message)s]'
    formatter = logging.Formatter(formatter_str, '%Y-%m-%d %H:%M:%S')
    logger.setLevel(debug_maping.get("debug"))

    fh = logging.FileHandler(os.path.join(sys.path[0], 'debug_new.log'))
    fh.setFormatter(formatter)
    for item in logger.handlers:#写之前确保文件关闭
        item.close()
        logger.removeHandler(item)
    logger.addHandler(fh)

    ch = logging.StreamHandler()#用于输出到控制台的handler
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
def sendAction(player_action):
    ws.send(json.dumps({
        "eventName": "__action",
        "data": {
            "action": player_action
        }
        })
        )
def sendBetAction(amount):
    ws.send(json.dumps({
        "eventName": "__action",
        "data": {
            "action": "bet",
            "amount": amount
        }
    }))    
def takeAction(action,player_name, data=None):
    try:
        global game_status
        global players_data_deal
        global players_data_flop
        global players_data_turn
        global players_data_river
        global chips
        global bigBlind
        global table_board
        global total_bet
        global myhandPoker
        if action == "__bet":
            chips = data["self"]["chips"]
            bigBlind=int(data['game']['bigBlind']['amount'])
            player_action = pokeCardJudge.judgeBetAction(data,game_status,total_bet,bigBlind)
            logging.debug("[round_action:"+str(player_action)+"]")
            if(player_action==pokeCardJudge.ALLIN or player_action==pokeCardJudge.RAISE or player_action==pokeCardJudge.CALL or player_action==pokeCardJudge.FOLD):
                 sendAction(player_action)
            else:
                 sendBetAction(int(player_action))
        elif action == "__action":
            begin=datetime.datetime.now()
            chips = data["self"]["chips"]
            round_name = data['game']['roundName'].lower()
            bigBlind=int(data['game']['bigBlind']['amount'])         
            myhandPoker =" ".join(data["self"]["cards"])
            if round_name == pokeCardJudge.ROUND_NAME_FLOP:
                player_action = pokeCardJudge.judgeFlopAction(data,game_status,total_bet,bigBlind)
            elif round_name == pokeCardJudge.ROUND_NAME_DEAL:#还未发公共牌
                player_action = pokeCardJudge.judgeDealAction(data,game_status,total_bet,bigBlind)
            elif round_name == pokeCardJudge.ROUND_NAME_TURN:
                player_action = pokeCardJudge.judgeTurnAction(data,game_status,total_bet,bigBlind)
            elif round_name == pokeCardJudge.ROUND_NAME_RIVER:
                player_action = pokeCardJudge.judgeRiverAction(data,game_status,total_bet,bigBlind)
            if(player_action==pokeCardJudge.ALLIN or player_action==pokeCardJudge.RAISE or player_action==pokeCardJudge.CALL or player_action==pokeCardJudge.FOLD):
                 sendAction(player_action)
            else:
                 sendBetAction(int(player_action))
            logging.debug("[round_name:"+str(player_action)+"----------the time is {}]".format((datetime.datetime.now()-begin).total_seconds()))
        elif action == "__new_peer":
            players = data
        elif action == "__new_round":
            logging.debug("[--------------new_round----------------]")
            players_data_deal = data["players"]
            game_status = 0
            del players_action[:]

        elif action == "__start_reload":
            if chips <100:
                takeAction("__reload",player_name=player_name)
        elif action == "__reload":
            ws.send(json.dumps({
                "eventName": "__reload"
            }))
        elif action == "__show_action":
            if len(table_board) != len(data["table"]["board"]):
                logging.debug("[show_action Hand {},Board:{}".format(myhandPoker,data["table"]["board"])+"]")
            table_board = data["table"]["board"]
            round_name = data["table"]["roundName"]
            total_bet=int(data["table"]["totalBet"])
            round_name = round_name.lower()
            str_players_action = ''.join(players_action).lower()
            if (data["action"]["action"] == 'raise'or data["action"]["action"] == 'allin' or data["action"]["action"] == 'bet') and str_players_action.find('raise') == -1 :
                    game_status = pokeCardJudge.DANGER
            players_action.append(data["action"]["action"])

        elif action == "__round_end":
            del players_data_deal[:]
            del players_data_flop[:]
            del players_data_turn[:]
            del players_data_river[:]
            del players_action[:]
            del table_board[:]
            game_status = 0

        elif action == "__game_over":
            logging.debug("[game over]")
        else:
            game_status
    except Exception as e:
        logging.error(traceback.format_exc())

def doListen(player_name,server_ip,server_port=None):
    try:
        global ws
        if server_port is not None:
            connect_str = "ws://{}:{}".format(server_ip,server_port)
        else:
            connect_str = "ws://{}".format(server_ip)
        ws = create_connection(connect_str)
        ws.send(json.dumps({
                "eventName": "__join",
                "data": {
                    "playerName": player_name
                }
            }))
        while 1:
            result = ws.recv()
            if(len(result)==0):
                continue
            msg = json.loads(result)
            event_name = msg["eventName"]
            data = msg["data"]
            #logging.error(data)
            takeAction(event_name,player_name, data)
    except Exception as e:
        logging.error(traceback.format_exc())
        player_name ="5d31cef4a8fe0fea70d7220079a4942a"
        server_ip = "10.64.8.72"
        #player_name ="aspire"
        #server_ip = "192.168.3.200"
        server_port = 80
        doListen(player_name,server_ip,server_port)


if __name__ == '__main__':
    init_logger()
    try:
        #http://pokerai.trendmicro.com.cn/   
        player_name ="5d31cef4a8fe0fea70d7220079a4942a"
        server_ip = "10.64.8.72"
        #player_name ="aspire"
        #server_ip = "192.168.3.200"
        server_port = 80
        doListen(player_name,server_ip,server_port)
    except KeyboardInterrupt:
        logging.error("Program exit by key board")
    
    