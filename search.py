import time
import logging
import clr
clr.AddReference("HandEvaluator")
from HoldemHand import Hand
from System import Array, Double, String, Int64
startingHandRecommendations=[
                [ 155,153 , 146, 145, 135, 63, 62, 61, 55, 55, 55, 55, 55 ], # AA AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s
                [ 152, 154, 135, 133, 133, 60, 59, 58, 57, 56, 55, 54, 53 ], # AKo KK KQs KJs KTs K9s K8s K7s K6s K5s K4s K3s K2s
                [ 145, 135, 153, 133, 133, 62, 56, 54, 54, 53, 52, 51, 50 ], # AQo KQo QQ QJs QTs Q9s Q8s Q7s Q6s Q5s Q4s Q3s Q2s
                [ 135, 61, 58, 148, 133, 56, 54, 52, 51, 50, 49, 48, 47 ], # AJo KJo QJo JJ JTs J9s J8s J7s J6s J5s J4s J3s J2s
                [ 63, 60, 57, 55, 147, 133, 54, 51, 49, 47, 46, 46, 45 ], # ATo KTo QTo JTo TT T9s T8s T7s T6s T5s T4s T3s T2s
                [ 61, 58, 56, 53, 52, 146, 62, 54, 48, 46, 44, 43, 42 ], # A9o K9o Q9o J9o T9o 99 98s 97s 96s 95s 94s 93s 92s
                [ 59, 56, 54, 52, 50, 48, 139, 62, 48, 45, 43, 41, 40 ], # A8o K8o Q8o J8o T8o 98o 88 87s 86s 85s 84s 83s 82s
                [ 59, 55, 52, 50, 48, 47, 46, 64, 48, 44, 42, 40, 38 ], # A7o K7o Q7o J7o T7o 97o 87o 77 76s 75s 74s 73s 72s
                [ 49, 49, 51, 48, 46, 45, 44, 43, 64, 43, 41, 40, 38 ], # A6o K6o Q6o J6o T6o 96o 86o 76o 66 65s 64s 63s 62s
                [ 49, 49, 50, 47, 44, 43, 42, 41, 40, 59, 41, 39, 38 ], # A5o K5o Q5o J5o T5o 95o 85o 75o 65o 55 54s 53s 52s
                [ 52, 49, 49, 46, 43, 41, 40, 39, 38, 38, 59, 38, 36 ], # A4o K4o Q4o J4o T4o 94o 84o 74o 64o 54o 44 43s 42s
                [ 52, 49, 48, 45, 42, 30, 38, 37, 36, 36, 34, 59, 35 ], # A3o K3o Q3o J3o T3o 93o 83o 73o 63o 53o 43o 33 32s
                [ 52, 49, 47, 44, 41, 39, 37, 35, 34, 34, 33, 31, 59 ]] # A2o K2o Q2o J2o T2o 92o 82o 72o 62o 52o 42o 32o 22

def getHandPower(handPoker):
    handPoker=handPoker.lower()
    if(len(handPoker)!=5):
        return -1
    isFlush=True if handPoker[1]==handPoker[4] else False
    x=converPoker(handPoker[0])
    y=converPoker(handPoker[3])
    if x<y:
       x,y=y,x
    if(isFlush):
         return startingHandRecommendations[y][x]
    else:
         return startingHandRecommendations[x][y]

def converPoker(ch):
    if ch=='a':
        return 0
    elif ch=='k':
        return 1
    elif ch =='q':
        return 2
    elif ch=='j':
        return 3
    elif ch=='t':
        return 4
    else:
        return 14-int(ch)
def  getRate(handPoker,boardPoker,numOpp):
    speed=0.1
    win=Hand.WinOdds(handPoker,boardPoker,"",numOpp,speed)
    _,ppotv,npotv=Hand.HandPotential(handPoker,boardPoker,Double(0), Double(0),numOpp,speed);
    hs=Hand.HandStrength(handPoker,boardPoker, numOpp, speed)
    ehs=hs*(1-npotv)+(1-hs)*ppotv
    #logging.debug("win:{:.5f},ppotv:{:.5f},npotv:{:.5f},hs:{:.5f},ehs{:.5f}".format(win,ppotv,npotv,hs,ehs))
    return win,ppotv,npotv,hs,ehs
    #return win
if __name__ == '__main__':
    while True:
        #handpoker= input("please input handpoker: ")
        #boardPoker=input("please input boardpoker: ")
        #numOpp=int(input("please input number: "))
        handpoker='7s 8d'
        boardPoker='4s 5d 6c'
        numOpp=3
        win,ppotv,npotv,hs,ehs=getRate(handpoker,boardPoker,numOpp)
        print(f'win:{round(win,5)} ppotv:{round(ppotv,5)} npotv:{round(npotv,5)} hs:{round(hs,5)} ehs:{round(ehs,5)}')