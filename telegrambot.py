import json
import requests as req
import time 
import datetime as dt 

TOKEN = "---"
Name = "Mat"
URL= "https://api.telegram.org/bot{}/".format(TOKEN)
ORARIO_URL = "https://corsi.unibo.it/magistrale/Physics/orario-lezioni/@@orario_reale_json?anno=1&amp;curricula=B25-000"

mysubjects = ["STATISTICAL MECHANICS","PHYSICS OF COMPLEX SYSTEMS",
            "PHYSICAL METHODS OF BIOLOGY","STATISTICAL DATA ANALYSIS FOR APPLIED PHYSICS",
            "IMAGE PROCESSING"]

def get_url(url):
    response = req.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_json_from_orario(orario):
    content = get_url(orario)
    Or = json.loads(content)
    return Or

def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js 

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id, last_update

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def loops():
    control = 0
    while True:
        time.sleep(0.5)
        updates = get_updates() #first dialogue
        last_message, chat_id, ctrl = get_last_chat_id_and_text(updates)
        if "/orario" in last_message and control != ctrl:
            control = ctrl 
            day_schedule = []
#            now = dt.datetime.now() 
#            today = str(now.day) + "/" + str(now.month) + "/"+ "20" + str(now.year)
            today = "22/10/2018"
            orario = get_json_from_orario(ORARIO_URL) #second dialogue 
            for x in range(len(orario["events"])):
                if orario["events"][x]["date_str"] == today:
                    if orario["events"][x]["title"] in mysubjects:
                        day_schedule.append(orario["events"][x]["title"] + " " +
                                            orario["events"][x]["time"])
                        day_schedule.append(today)
            send_message(day_schedule, chat_id)
            
loops()

#def react_to_ciao():
#    control = 0
#    while True:
#        time.sleep(0.01)
#        text, chat, var = get_last_chat_id_and_text(get_updates())
#        if text == "/ciao" and control != var: 
#            control = var
#            send_message("Ciao :D, La data è " + 
#                        str(datetime.datetime.now()),
#                        chat)


    
#react_to_ciao()     
#text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text, chat)
