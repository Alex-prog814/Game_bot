from token_for_bot import TOKEN
import telebot
from telebot import types
from PIL import Image
from threading import Thread
import urllib.request, urllib.parse
import csv
import datetime
import schedule
import time
import random


token = TOKEN
bot = telebot.TeleBot(token)

attempts = 3

#start keyboard
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
k1 = types.KeyboardButton('Играть')
k2 = types.KeyboardButton('Ноу')
keyboard.add(k1, k2)

@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    try:
        random_int = random.choice(list(range(1,11)))
        print(random_int)
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, f'Привет {message.chat.first_name}, начнем веселье', reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_start, random_int)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'ooops!!')

def get_start(message, random_int):
    chat_id = message.chat.id
    if message.text == 'Играть':
        msg = bot.send_message(chat_id, f'Ок, тогда вот правила, правило только одно: ВЫЖИТЬ,\n'
                                    'ну а если серьезно, то нужно угадать число от 1 до 10 за три попытки\n'
                                    'угадал-красавчеГ, не угадал-не красавчеГ, соответственно)\n\n'
                                    '/ok, если прочитал(-а)')
        bot.register_next_step_handler(message, game, attempts, random_int)
    else:
        bot.send_message(chat_id, f'Странный ты человек {message.chat.first_name}, ладно, увидимся...')

def game(message, attempts, random_int):
    attempts = attempts - 1
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Погнали, выбери число от 1 до 10 ...')
    bot.register_next_step_handler(msg, check_answer, attempts, random_int)

def check_answer(message, attempts, random_int):
    chat_id = message.chat.id
    if message.text != str(random_int):
        msg = bot.send_message(chat_id, f'Все фигня, давай по-новой')
        if attempts == 0:
            msg = bot.send_message(chat_id, f'Чел, сорян, видимо не сегодня...\n'
                                            'Начать заново? /start')
            bot.register_next_step_handler(msg, start_message)
        else:
            game(msg, attempts, random_int)
    else:
        msg = bot.send_message(chat_id, f'Базар жок - красавчеГ, твое имя записано золотыми буквами в гугл шитс\n'
                                        '/end для завершения')
        bot.register_next_step_handler(msg, write_to_sheets)

def write_to_sheets(message):
    url = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSctrulXMks6o9qvd6fubV4ZZoKi2ERcUFwnyTRdHuVg3leJQA/formResponse"
    data = {
        'entry.1884265043': message.chat.first_name, 
        }
    data = bytes(urllib.parse.urlencode(data).encode())
    handler = urllib.request.urlopen(url, data)

bot.polling(none_stop=True, timeout=3600)
