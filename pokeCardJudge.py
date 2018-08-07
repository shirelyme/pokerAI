#! /usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import search
import json
import player
ALLIN ="allin"
RAISE = "raise"
CALL ="call"
FOLD = "fold"
CHIPS = "chips"

RISK = 1
DANGER = 2

ROUND_NAME_DEAL = 'deal'
ROUND_NAME_FLOP = 'flop'
ROUND_NAME_TURN = 'turn'
ROUND_NAME_RIVER = 'river'

def convertPokerToIndex(poker):
    pokerResult=[]
    pokerType=-1
    for i in poker:
        if(i[1]=='H'):
            pokerType=0
        elif(i[1]=='S'):
            pokerType=1
        elif(i[1]=='C'):
            pokerType=2
        else:
            pokerType=3
        pokerResult.append(pokerType*13+pokerSize)
    return pokerResult

def convertPokerValue(value):
    pokerSize=-1
    value = value.lower()
    if(value=='T'.lower()):
        pokerSize=8
    elif(value=='J'.lower()):
        pokerSize=9
    elif(value=='Q'.lower()):
        pokerSize=10
    elif(value=='K'.lower()):
        pokerSize=11
    elif(value=='A'.lower()):
        pokerSize=12
    else:
        pokerSize=int(value)-2
    return pokerSize

def convertPokerHexValue(value):
    pokerSize=-1
    value = value.lower()
    if(value=='T'):
        pokerSize=8
    elif(value=='J'):
        pokerSize=9
    elif(value=='Q'):
        pokerSize='a'
    elif(value=='K'):
        pokerSize='b'
    elif(value=='A'):
        pokerSize='c'
    else:
        pokerSize=int(value)-2
    return pokerSize

def getSurviveNum(data):
    num=0
    return 4
    for i in data:
        num+=1
    return num-1

def judgeWin5(win,minBet,bigBlind):
    if(win>0.95):
        return 5*minBet
    elif(win>0.80):
        return 3*minBet
    elif(win>0.70):
        return 2*minBet
    elif(win>0.60):
        return CALL
    elif(win>=0.12):
        return CALL
    else:
        return FOLD
def judgeWin15(win,minBet,bigBlind):
    if(win>0.90):
        return 8*minBet
    elif(win>0.70):
        return 5*minBet
    elif(win>0.50):
        return 4*minBet
    elif(win>0.30):
        return CALL
    elif(win>=0.11):
        return CALL
    else:
        return FOLD
      
def judgeWin35(win,minBet,bigBlind):
    if(win>0.88):
        return 10*minBet
    elif(win>0.65):
        return 5*minBet
    elif(win>0.45):
        return 2*minBet
    elif(win>0.4):
        return CALL
    elif(win>=0.13):
        return CALL
    else:
        return FOLD
def judgeBetAction(data,gameStaues,totalBet,bigBlind):
    handPoker =" ".join(data["self"]["cards"])
    boardPoker=" ".join(data['game']['board'])
    minBet=int(data["self"]["minBet"])
    chips=int(data["self"]["chips"])
    numPeople = getSurviveNum(data['game']["players"])
    win,pp,npotv,hs,ehs=search.getRate(handPoker,boardPoker,numPeople)
    if pp<0.05 and win>0.89 and hs>0.80:
        return chips*0.75
    bf=getBenefit(minBet,totalBet,win,chips)
    if gameStaues==DANGER:
        win-=0.01*numPeople
    if chips>18000:
        if bf<5:
            return FOLD
        else:
            return minBet
    else:
        if bf<1:
            return FOLD
        elif bf<5:
            return judgeWin5(win,minBet,bigBlind)
        elif bf<15:
            return judgeWin15(win,minBet,bigBlind)
        elif bf<35:
            return judgeWin35(win,minBet,bigBlind)
        else:
            return minBet

def judgeRiverAction(data,gameStaues,totalBet,bigBlind):#5张公牌
    handPoker =" ".join(data["self"]["cards"])
    boardPoker=" ".join(data['game']['board'])
    minBet=int(data["self"]["minBet"])
    numPeople = getSurviveNum(data['game']["players"])
    chips=int(data["self"]["chips"])
    win,ppotv,npotv,hs,ehs=search.getRate(handPoker,boardPoker,numPeople)
    one_chips=chips/minBet
    benefit=getBenefit(minBet,totalBet,win,chips)
    bf=getBenefit(minBet,totalBet,win,chips)
    if gameStaues==DANGER:
        win-=0.005*numPeople
    if chips>18000:
        if bf<5:
            return FOLD
        else:
            return minBet
    else:

        if bf<0.7:
            return FOLD
        elif bf<5:
            return judgeWin5(win,minBet,bigBlind)
        elif bf<15:
            return judgeWin15(win,minBet,bigBlind)
        elif bf<35:
            return judgeWin35(win,minBet,bigBlind)
        else:
            return minBet
    

def judgeTurnAction(data,gameStaues,totalBet,bigBlind):#4张公牌
    handPoker =" ".join(data["self"]["cards"])
    boardPoker=" ".join(data['game']['board'])
    minBet=int(data["self"]["minBet"])
    numPeople = getSurviveNum(data['game']["players"])
    chips=int(data["self"]["chips"])
    win,ppotv,npotv,hs,ehs=search.getRate(handPoker,boardPoker,numPeople)
    one_chips=chips/minBet
    benefit=getBenefit(minBet,totalBet,win,chips)
    bf=getBenefit(minBet,totalBet,win,chips)
    if gameStaues==DANGER:
        win-=0.01*numPeople
    if chips>18000:
        if bf<5:
            return FOLD
        else:
            return minBet
    else:

        if bf<0.8:
            return FOLD
        elif bf<5:
            return judgeWin5(win,minBet,bigBlind)
        elif bf<15:
            return judgeWin15(win,minBet,bigBlind)
        elif bf<35:
            return judgeWin35(win,minBet,bigBlind)
        else:
            return minBet


def judgeFlopAction(data,gameStaues,totalBet,bigBlind):#3张公牌
    handPoker =" ".join(data["self"]["cards"])
    boardPoker=" ".join(data['game']['board'])
    minBet=int(data["self"]["minBet"])
    numPeople = getSurviveNum(data['game']["players"])
    chips=int(data["self"]["chips"])
    win,ppotv,npotv,hs,ehs=search.getRate(handPoker,boardPoker,4)#flop阶段适当增大胜率
    one_chips=chips/minBet
    bf=getBenefit(minBet,totalBet,win,chips)

    if chips>18000:
        if bf<5:
            return FOLD
        else:
            return minBet
    else:

        if bf<0.5:
            return FOLD
        elif bf<5:
            return judgeWin5(win,minBet,bigBlind)
        elif bf<15:
            return judgeWin15(win,minBet,bigBlind)
        elif bf<35:
            return judgeWin35(win,minBet,bigBlind)
        else:
            return minBet

def getBenefit(minBet,totalBet,win,chips):
    pot=(minBet+1)/float(minBet+totalBet+1)
    benefit=win/pot
    logging.debug("[round_benefit: benefit:{:.5f},win:{:.5f},minBet:{},totalBet:{}]".format(benefit,win,minBet,totalBet))
    return benefit
def max(a,b):
    return a if a>b else b

def judgeDealAction(data,gameStaues,totalBet,bigBlind):#还未发公牌,两张牌按照起手规则打
    handPoker =" ".join(data["self"]["cards"])
    boardPoker=" ".join(data['game']['board'])
    minBet=int(data["self"]["minBet"])
    numPeople = getSurviveNum(data['game']["players"])   
    chips=int(data["self"]["chips"])
    hs=search.getHandPower(handPoker)
    logging.debug(f"Deal Round:{handPoker} ,HS:{hs} minBet:{minBet}")
    if minBet>150:
        if chips>18000:
            if hs>130:
                return 200
            else:
                return FOLD
        if hs>130:
            return max(3*minBet,200)
        elif hs>=60:
            return max(minBet,200)
        elif hs>=55:
            return max(minBet,100)
        elif hs>46:
            return CALL
        else:
            return FOLD
    else:
        if chips>18000:
            if hs>130:
                return 200
            else:
                return FOLD
        if hs>150:
            return ALLIN
        elif hs>130:
            return max(3*minBet,200)
        elif hs>=60:
            return max(minBet,200)
        elif hs>=55:
            return max(minBet,100)
        else:
            if minBet<200:
                return CALL
            else:
                return FOLD