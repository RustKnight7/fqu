import telebot
import random
import time, re
import time
import pyowm
import requests
from mqtt import *
import datetime
import reader
import os
from dotenv import load_dotenv

token=load_dotenv()
token = os.getenv('TOKEN')
print(token)

commandlist = {'/start': 'start_message(message)', '/help' : 'help_message(message)', '/rzd' : 'rzd_message(message)', '/weather' : 'weather_message(message)', '/music' : 'music_message(message)'}

lovestickerpack = ['CAADAgAD-wUAAtJaiAEK_F4c8hn9yxYE', 'CAADAgADcgkAAgi3GQIEU9tYxpNH9xYE', 'CAADAgADEgYAAtJaiAH3r7K1PEN3dBYE', 'CAADAgADgQkAAgi3GQJMZcFWk15u8RYE', 'CAADAgADgwkAAgi3GQKYlDU84Ixx3RYE', 'CAADAgADGgYAAtJaiAEu2wLZUu4NEBYE', 'CAADAgADBQADwDZPE_lqX5qCa011FgQ', 'CAADAgADFQADwDZPE81WpjthnmTnFgQ', 'CAADAgADBgADwDZPE8fKovSybnB2FgQ', 'CAADAgADFgADwDZPE2Ah1y2iBLZnFgQ', 'CAADAgADDQADwDZPE6T54fTUeI1TFgQ', 'CAADAgAD0wADVp29CvUyj5fVEvk9FgQ']

questionstickerpack = ['CAADAgADEAADwDZPE-qBiinxHwLoFgQ', 'CAADAgADEgADwDZPEzO8ngEulQc3FgQ', 'CAADAgADFwYAAtJaiAFCOa9AJUzy7RYE', 'CAADAgADLAYAAtJaiAES51iRyPvrxBYE', 'CAADAgAD4wADVp29Cg_4Isytpgs3FgQ', 'CAADAgADdAAD9wLIDwfMgh3wvMzzFgQ', 'CAADAgADegkAAgi3GQI5G6atKdU53BYE']

loadstickerpack = ['CAADAgADjwADFkJrCr24snHVnwbiFgQ', 'CAADAgADGAADwDZPE9b6J7-cahj4FgQ', 'CAADAgADewAD9wLID0X7aCG8iMvfFgQ', 'CAADAgAD5QADVp29CggLFmSVBdGKFgQ', 'CAADAgAD4QADVp29ClvBlItA-NOgFgQ', 'CAADAgADwAADVp29Ct1dnTI9q-YvFgQ', 'CAADAgAD1QADVp29CveXwRdcmk7nFgQ', 'CAADAgADkgADFkJrCqRKrRN_PIQxFgQ']

angrystickerpack = ['CAADAgADywADVp29CllGpcs9gzQoFgQ', 'CAADAgADIAADwDZPE_QPK7o-X_TPFgQ', 'CAADAgADfQAD9wLIDy7JuwrdyyJJFgQ', 'CAADAgADnwADFkJrCg3fpq5eaUiCFgQ']

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/start', '/help', '/weather', '/rzd', '�����-���������', '������', '5.12.2019')
keyboard1.row('/music')

owm = pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = 'ru')
bot = telebot.TeleBot(token)

fromplace = str()
toplace = str()
dateregistration = str()
status=''

@bot.message_handler(commands=['rzd'])

def rzd_message(message):
    bot.send_message(message.chat.id, '������� ����� �����������')
    bot.register_next_step_handler(message, from_place_registration)
def from_place_registration(message):
    global commandlist
    global fromplace
    if message.text not in commandlist:
        fromplace = message.text
        bot.send_message(message.chat.id, '������� ����� ����������')
        bot.register_next_step_handler(message, to_place_registration)
    else:
        exec(commandlist[message.text])
def to_place_registration(message):
    global commandlist
    global toplace
    if message.text not in commandlist:
        toplace = message.text
        bot.send_message(message.chat.id, '������� ���� �����������')
        bot.register_next_step_handler(message, date_registration)
    else:
        exec(commandlist[message.text])
def date_registration(message):
    global commandlist
    global fromplace
    global toplace
    global dateregistration
    global loadsticerpack
    if message.text not in commandlist:
        dateregistration = message.text
        bot.send_sticker(message.chat.id, random.choice(loadstickerpack))
        bot.send_message(message.chat.id, '��� ������ �� ���������� �����������')
        print(fromplace)
        print(toplace)
        print(dateregistration)
        Sendler(fromInput=fromplace,fromOutput=toplace,date=dateregistration).send()
        bot.send_message(message.chat.id, '��������������� �������� �� ����� �����������: '+"\n"+reader.read())
    else:
        exec(commandlist[message.text])    
    
    
@bot.message_handler(commands=['start'])

def start_message(message):
    global lovestickerpack
    bot.send_message(message.chat.id, '������!\n���� �����...�������, � �� �������� ���\n��� ������ ���� ������� �� ������ ������:\n1./start\n2./weather\n3./help\n4./rzd', reply_markup=keyboard1)
    bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
    
@bot.message_handler(commands=['weather'])

def weather_message(message):
    bot.send_message(message.chat.id, '�� �����')
    bot.register_next_step_handler(message, weather_information)
def weather_information(message):
    place=''
    global status
    global angrystickerpack
    if message.text not in commandlist:
        try:
            place = message.text.lower()
            observation = owm.weather_at_place(place)
            weather = observation.get_weather()
            status = weather.get_detailed_status()
            temp = weather.get_temperature('celsius')['temp']
            wind = weather.get_wind()['speed']
            print(weather)
            bot.send_message(message.chat.id, "������ ������ " + message.text + "\n�����������: " + str(temp) + "�C" + "\n�� �����: " + str.title(status) + "\n�������� �����: " + str(wind) + "�/c")
            if temp >= 15:
                bot.send_message(message.chat.id, "������-mood: C����-�� ")
            elif 15 > temp  and temp > 0:
                bot.send_message(message.chat.id, "������-mood: ������ ��� ������ �� ���� ")
            elif temp < 0 and -25 < temp:
                bot.send_message(message.chat.id, "������-mood: �������� ����, ���� ������� ")
            elif temp <= -25:
                bot.send_message(message.chat.id, "������-mood: �� �����, ���� �����")
        except pyowm.exceptions.api_response_error.NotFoundError:
            bot.reply_to(message, '�����, ������ ������ ��� �� ������')
            bot.send_sticker(message.chat.id, random.choice(angrystickerpack))
    else:
        exec(commandlist[message.text])
    
@bot.message_handler(commands=['help'])
def help_message(message):
    global lovestickerpack
    bot.send_message(message.chat.id, '1./start - ��� ������� ��������� ��� �������� ��� ������ � ��������� � �������� �����\n2./weather - ��������� ��� ������ ��������� ������ � ������ �����\n3./help - ���  ������� ��������� ����� ������')
    bot.send_sticker(message.chat.id,random.choice(lovestickerpack))
    
@bot.message_handler(commands=['music'])
def music_message(message):
    for i in range(3):
        n=random.randint(1,2)
        audio = open(str(n)+".mp3", mode='rb')
        print("opened "+str(n)+".mp3")
        bot.send_audio(message.from_user.id,audio, timeout=1000)  
@bot.message_handler(content_types=['text'])

def text_analyze(message):
    global lovestickerpack
    global angrystickerpack
    global questionstickerpack
    if '������' in message.text.lower():
        bot.reply_to(message, '� ���� ������� �������� "������" ����� �� ������ �����, ���� �� ������� ���� ������ ������ �������')
        bot.send_sticker(message.chat.id, random.choice(lovestickerpack))
    elif '�����' in message.text.lower() or '�����' in message.text.lower():
        bot.reply_to(message, '�����...�����...������ ��� ���-�� ����������')
        bot.send_sticker(message.chat.id, random.choice(angrystickerpack))
    elif message.text.lower():
        bot.reply_to(message, '� ���� �� � ��������� ������ ���� �����')
        bot.send_sticker(message.chat.id, random.choice(questionstickerpack))
bot.polling()