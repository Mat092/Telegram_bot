import json
import requests as req
import time 
import datetime

TOKEN = ""
Name = "Mat"
URL= "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = req.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js 

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text,chat_id,last_update)

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def react_to_ciao():
    control = 0
    while True:
        time.sleep(0.01)
        text, chat, var = get_last_chat_id_and_text(get_updates())
        if text == "/ciao" and control != var: 
            control = var
            send_message("Ciao :D, La data è " + 
                        str(datetime.datetime.now()),
                        chat)
    
react_to_ciao()    
    
#text, chat = get_last_chat_id_and_text(get_updates())
#send_message(text, chat)
