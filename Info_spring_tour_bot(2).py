
# coding: utf-8

# In[ ]:


import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from random import choice
import json
import random
import time

#自行更新  #自行更新   #自行更新
TOKEN = '515307683:AAH0TWRT57mBfzHsHHJHZ_aMP1sZwwNr3Tg'             #自行更新
password = '9487'      #自行更新
#自行更新  #自行更新   #自行更新

bot = telepot.Bot(TOKEN)

# task[number<int>] = { ans:<string>, score<:int>, }
task = {}
# self[username<sting>] = {team<int>, score:<int>, }
self = {}
# team[team_number<int> = {members<list>, total<int>, task:[<int finish<bool>]}, bounus:<int>, }
team = {1:{
          #"task_number" : 0, 
          "members":[], 
          "total":0},
        2:{
          #"task_number" : 0, 
          "members":[], 
          "total":0},
        3:{
          #"task_number" : 0, 
          "members":[], 
          "total":0},
        4:{
          #"task_number" : 0, 
          "members":[], 
          "total":0},
        5:{
          #"task_number" : 0, 
          "members":[], 
          "total":0},
        6:{
          #"task_number" : 0, 
          "members":[], 
          "total":0}
        }

# 列印訊息接收log
def print_msg(msg):
    print(json.dumps(msg, indent=4))

# 接收chat後執行：
def on_chat(msg):
    # 得取基礎資料：訊息類型\聊天室總類\聊天室id
    header = telepot.glance(msg, flavor="chat")
    print_msg(msg)
    data=""
    if header[0] == "text":
        text = msg["text"]
        username = msg["from"]["username"]
        try:
            userteam = self[username]["team"]
        except:
            print("userteam err")
        
        # command
        if text.startswith("/"):
            command = text.lstrip("/")
            
            if command == "start":
                text = "OK， {}\n你準備好了...... 讓我們開始一場奇幻冒險ㄅ OwO"
                bot.sendMessage(header[2], text.format(msg["from"]["first_name"]))
                bot.sendMessage(header[2], "請先輸入您的組別 /team <阿拉伯數字>～\n請小心輸入，這會影響你的計分唷～")
                bot.sendMessage(header[2], "請輸入/list查看得分紀錄，輸入/total 獲取總計分！")
                bot.sendMessage(header[2], "/ans <題號><答案> 回傳任務答案\n/total 獲取總計分\n/list 查看完整小隊資訊\n")
            
            # user設定組別
            elif command[:4] == "team":
                data = command[4:].split()
                data=int(data[0])
                if username in self:
                    if username in team[data]["members"]:
                        bot.sendMessage(header[2], "ni已經註冊過ㄖ")
                    else:
                        team[self[username][team]].remove(username)
                        team[data]['members'].append(username)
                        send = "Hello, Your new partner are :"
                        for j in team[data]:
                            send += j
                            send += "\n"
                        bot.sendMessage(header[2], send)
                else:
                    self[username] = {"team" : data}
                    team[data]['members'].append(username)
                    send = "Hello, Your partner are :"
                    if len(team[data]["members"]) == 1:
                        bot.sendMessage(header[2], "You are the First!\nGo to help your other partners!")
                    if len(team[data]["members"]) == 2:
                        bot.sendMessage(header[2], "You are the Second!\nGo to help your other partners!")    
                    for j in team[data]["members"]:
                        send += j
                        send += "\n"
                    bot.sendMessage(header[2], send)
                    
            # manager 設定題目        
            elif command[:3] == "add":
                data = command[3:].split()
                if len(data) == 4:
                    if data[0] == password:
                        if data[2] == 'x':
                            data[2] = random.randrange(0, 1080503, 2)
                        task[data[1]] = {"ans" : data[2], "score" : int(data[3]) }
                        bot.sendMessage(header[2], "Thank you! We have add it to our data base.")
                    else:
                        bot.sendMessage(header[2], "Please enter the true password !")
                else:
                    bot.sendMessage(header[2], "Please enter the correct data!\n/add <password> <task_number> <task_answer> <task_score> !")

            # user answer the question                     
            elif command[:3] == "ans":
                data = command[3:].split()
                task_number = data[0]
                task_answer = data[1]
                if (not task_number in team[userteam]) or (team[userteam][task_number] >=-3) or (team[userteam][task_number] <-3 and time.time() >= team[userteam]["penalty"]) :                        
                    if task[task_number]["ans"] == task_answer:
                        if task_number in team[userteam]:
                            if team[userteam][task_number] == 1:
                                bot.sendMessage(header[2], "You have sended the correct answer...\nGo on to find the next task! ouo")
                            else:
                                team[userteam][task_number] = 1
                                team[userteam]["total"] += task[task_number]["score"]
                                bot.sendMessage(header[2], "Congratulations! You answered the correct answer!\nGo on to find the next task!")
                        else:
                            team[userteam][task_number] = 1
                            team[userteam]["total"] += task[task_number]["score"]
                            bot.sendMessage(header[2], "Congratulations! You answered the correct answer!\nGo on to find the next task!")
                    else:
                        if task_number in team[userteam] and team[userteam][task_number] != 1:
                            if team[userteam][task_number] % 3 == 0:
                                team[userteam]["penalty"] = time.time()+60
                                team[userteam][task_number] -= 1
                                bot.sendMessage(header[2], "You have sent too many answers,\nplease wait " +  str(int(team[userteam]["penalty"]-time.time())) + " seconds and try again!")
                            else:
                                team[userteam][task_number] -= 1
                                bot.sendMessage(header[2], "Sorry... It's also not correct answer. QAQ")
                        else :
                            team[userteam][task_number] = -1
                            bot.sendMessage(header[2], "Sorry... It's not correct answer 0.0")
                else:
                    bot.sendMessage(header[2], "You have sent too many answers,\nplease wait " +  str(int(team[userteam]["penalty"]-time.time())) + " seconds and try again!")
            # user request the list of team info
            elif command[:4] == "list":
                for i in team[userteam]:
                    send = ""
                    if i == "members":
                        send += "partner : "
                        for j in team[userteam][i]:
                            send += j
                            send += " "
                        send += "\n"
                    elif i == "total":
                        send = "你隊伍的總分為：" + str(team[userteam][i]) + "分"
                    elif i == "penalty":
                        send = "你的懲罰時間為：" + str(team[userteam][i]) + "秒"
                    else:
                        send = "第 " +str(i) + " 題通過！"
                    bot.sendMessage(header[2], send)
                    
            # user request the total score of team        
            elif command[:5] == "total":
                bot.sendMessage(header[2],"Your total score is "+ str(team[userteam]['total']) + ".")
            
            # /bonus <username> <score>
            elif command[:5] == "bonus":
                data = command[5:].split()
                bonus_user = data[0]
                bonus_score = int(data[1])
                userteam = self[bonus_user][team]
                team[userteam]["total"] += bonus_score
                bot.sendMessage(header[2],"Congratulations! team " + userteam + " got " + str(bonus_score) + "scores!")

            # /ac <username> <task_number>
            elif command[:2] == "ac":
                data = command[2:].split()
                userteam = self[data[0]][team]
                team[userteam][data[1]] = True
                team[userteam]["total"] += task[data[1]][score]
                bot.sendMessage(header[2],"Congratulations! team " + userteam + " send the correct answer!")
                                
            
                                
MessageLoop(bot, {
    'chat': on_chat,
    #'callback_query': on_callback_query,
}).run_as_thread()

print('Listening ...')

