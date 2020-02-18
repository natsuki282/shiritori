# coding:UTF-8
import socket
import string
import time
import subprocess
import shlex
import json
import random
import sys
import time

host = "localhost"
port = 10060

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

array=[]
CMD_SAY = './module/jtalk.sh'
dic_words=[]
small_words=[["っ","つ"],["ゃ","や"],["ゅ","ゆ"],["ょ","よ"],["ぁ","あ"],["ぃ","い"],["ぅ","う"],["ぇ","え"],["ぉ","お"],["ゎ","わ"]]
used_words=[]

'''
def write_file():
    with open("result.txt","wt") as f:
        for w in array:
            f.write(w+"\n")
'''

def read_dec():
    with open("./module/dictionary2.txt","r") as dic_f:
        buff=dic_f.read().split("\n")
        for i in range(69):
            temp=buff[i].split("，")
            dic_words.append(temp)
    dic_f.close()
    with open("./module/index.txt","r") as user_dic:
        buffer=user_dic.read().split("\n")
        for i in range(69):
            temper=buffer[i].split("，")
            used_words.append(temper)
    user_dic.close()

def shiritori(player_word):
    t=1
    for i in range(69):
        if player_word[len(player_word)-1]=="ー":
            t=2
        search=player_word[len(player_word)-t]
        for j in range(9):
            if player_word[len(player_word)-t]==small_words[j][0]:
                search=small_words[j][1]
        if search==dic_words[i][0]:
            if len(dic_words[i])!=1:
                rand=random.randint(1,len(dic_words[i])-1)
                #もし最後の文字がんだったら
                if dic_words[i][rand].endswith('ん'):
                    say(dic_words[i][rand])
                    say("あっ、んがついたので私のまけです") #負けたときの言葉
                    sys.exit()
                else:
                    say(dic_words[i][rand])
                    player_word=check(dic_words[i][rand])
                    used_words[i].append(dic_words[i][rand])
                    del dic_words[i][rand]
            else:
                say("単語がなくなりました、私のまけです")
                sys.exit()
            return player_word

def listen():
    print("\rYOUR TURN  >>> ",end='')
    s.sendall(b"RESUME\n")
    data = ""
    while(data.find('</SHYPO>') == -1):
        data += s.recv(1024).decode("utf-8")
        time.sleep(1)
        ###player_word=''
        for line in data.split('\n'):
            index = line.find('WORD=')
            if index != -1:
                line = line[index + 6: line.find('"',index + 6)]
                if line != '[s]' and line != '[/s]':
                    player_word = line
                    print(player_word)
                    ###socket.sendall(b"PAUSE\n")
                    flag = input("Is this right? [Enter/n] ")
                    if flag == "":
                        array.append(player_word)
                        return player_word
                    else:
                        player_word=''
                        return listen()

def check(word):
    player_word=listen()
    ###import pdb; pdb.set_trace()
    while word[len(word)-1]!=player_word[0]:
            say(word[len(word)-1]+"からはじまって")
            time.sleep(1)
            player_word=listen()
    for i in range(69):
        if player_word[0]==used_words[i][0]:
            stock=i
            break
    for i in range(len(used_words[stock])-1):
        if player_word==used_words[stock][i+1]:
            say("それ、さっき言ったから私の勝ち")
            sys.exit()
    used_words[stock].append(player_word)
    for i in range(len(dic_words[stock])-2):
        if player_word==dic_words[stock][i+1]:
            del dic_words[stock][i+1]
    if player_word.endswith("ん")==True:
        say("ざんねん、私のかちです")
        write_file()
        sys.exit()
    return player_word

def say(text):
    print("raspberry pi : " + text)
    text = CMD_SAY + ' ' + text
    proc = subprocess.Popen(shlex.split(text))
    proc.communicate()
    return



### Execute
if __name__ == "__main__":
    try:
        s.sendall(b"PAUSE\n")
        read_dec()
        word="しりとり"
        say(word)
        word=check(word)
        while True:
            word=shiritori(word)
    except KeyboardInterrupt:
        #write_file()
        print("disconnect")
        s.close()

