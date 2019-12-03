#!/usr/bin/env python
# -*-cording:utf-8-*-

import shlex
import subprocess
import json
import random
import sys

CMD_SAY='./jtalk.sh'
dic_words=[]

def read_dec():
    with open("dictionary2.txt","r") as dic_f:
        buff=dic_f.read().split("\n")
        for i in range(69):
            temp=buff[i].split("，")
            dic_words.append(temp)
def say(text):
    text = CMD_SAY + ' ' + text
    print(text)
    proc = subprocess.Popen(shlex.split(text))
    proc.communicate()
    return



def shiritori(player_word):


    for i in range(69):
        if player_word[len(player_word)-1]==dic_words[i][0]:
            if len(dic_words[i])==1:
                say("単語がなくなりました")
                sys.exit()
            else:
                rand=random.randint(1,len(dic_words[i])-1)
                say(dic_words[i][rand])
                buff=dic_words[i][rand]
                del dic_words[i][rand]
                return buff

if __name__ == "__main__":
    read_dec()

    word=input("最初の字>")
    try:
        while True:
            word=shiritori(word)
    except KeyboardInterrupt:
        pass
