
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


#自行更新  #自行更新   #自行更新
TOKEN = ''             #自行更新
password = '9487'      #自行更新
#自行更新  #自行更新   #自行更新

bot = telepot.Bot(TOKEN)

# task[number<int>] = { ans:<string>, score<:int>, }
task = {}
# self[username<sting>] = {team<int>, score:<int>, }
self = {}
# team[team_number<int> = {members<list>, total<int>, task:[<int finish<bool>]}, bounus:<int>, }
team = {1:{
          #"task_number" : False, 
          "members":[], 
          "total":0},
        2:{},
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
                bot.sendMessage(header[2], "/ans<題號><答案> 回傳任務答案\n/total 獲取總計分\n/list 查看完整小隊資訊\n")
            
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
                        bot.sendMessage(header[2], "Your the First!\nGo to help your other partners!")
                    if len(team[data]["members"]) == 2:
                        bot.sendMessage(header[2], "Your the Second!\nGo to help your other partners!")    
                    for j in team[data]["members"]:
                        send += j
                        send += "\n"
                    bot.sendMessage(header[2], send)
                    
            # manager 設定題目        
            elif command[:3] == "add":
                data = command[3:].split()
                if len(data) == 4:
                    if data[0] == password:
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
                if task[task_number]["ans"] == task_answer:
                    if task_number in team[userteam]:
                        bot.sendMessage(header[2], "You have sended the correct answer...\nGo on to find the next task! ouo")
                    else:
                        team[userteam][task_number] = True
                        team[userteam]["total"] += task[task_number]["score"]
                        bot.sendMessage(header[2], "Congratulations! You answered the correct answer!\nGo on to find the next task!")
                else:
                    bot.sendMessage(header[2], "Sorry... It's not correct answer 0.0")
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
                    else:
                        send = "第 " +str(i) + " 題通過！"
                    bot.sendMessage(header[2], send)
                    
            # user request the total score of team        
            elif command[:5] == "total":
                bot.sendMessage(header[2],"Your total score is "+ str(team[userteam]['total']) + ".")

MessageLoop(bot, {
    'chat': on_chat,
    #'callback_query': on_callback_query,
}).run_as_thread()

print('Listening ...')

