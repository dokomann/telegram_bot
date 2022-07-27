import requests
import json

from datetime import *
from time import sleep

global OFFSET
OFFSET = 0

botToken = "5415293109:AAGtvCvpGEs6WpHecX4aMXqerP8B4WqX9vc"

global requestURL
global sendURL

requestURL = "https://api.telegram.org/bot" + botToken + "/getUpdates"
sendURL = "https://api.telegram.org/bot" + botToken + "/sendMessage"
sendPhotoURL = "https://api.telegram.org/bot" + botToken + "/sendPhoto"

imageURL = r"/home/assi/Python/logo.png"

def update (url):
    global OFFSET

    try:
        update_raw = requests.get(url + "?offset=" + str(OFFSET))
        #update_raw = requests.get(url)
        update = update_raw.json()
        result = extract_result(update)
        #print (result)

        if result != False:
            OFFSET = result['update_id'] + 1
            return result
        else:
            return False

    except requests.exceptions.ConnectionError:
        pass

def extract_result (dict):
    result_array = dict['result']
    
    if result_array == []:
        return False
    else:
        result_dic = result_array[0]
        print (result_array[0])
        # print (result_array[1]) nur wenn zwischenzeitlich mehr eingegangen ist
        return result_dic

def uhrzeit ():
    start = datetime.now()
    start = start + timedelta(minutes=360)
    zeit = start.strftime("%H:%M")
    print (zeit)
    return zeit 

def send_message (chatID, message):
    zeit = uhrzeit() + " " + message
    data = {'chat_id': chatID, 'text': zeit}
    response = requests.post(sendURL, data=data)
    print (response.request.url)
    print (response.request.headers)
    print (response.request.body)

def send_photo (chatID, photo, caption):
    print ("Sending picture ...")  
    zeit = uhrzeit()  + " " + caption
    params = {'chat_id': chatID, 'caption':zeit }
    img = {'photo': open(imageURL, 'rb')}    
    requests.post(sendPhotoURL, params=params, files=img)
    

while True:
    newmessage = update (requestURL)
    #print (newmessage)

    try:

        if newmessage != False:
            userchatid = newmessage['message']['chat']['id']
            usertext = newmessage['message']['text']
            username = newmessage['message']['from']['first_name']

            if usertext.lower() in ["hi", "hello", "hallo", "Hey", "/start"]:
                send_message(userchatid, "Hi " + username)
            elif usertext.lower() in ["logo", "pic", "bild", "snap"]:
                send_photo(userchatid, imageURL, "Das ist das Logo")
            else:
                send_message(userchatid, "You said: " + usertext)
                #break
    
    except Exception as e:
        print(e)

    sleep (1)


