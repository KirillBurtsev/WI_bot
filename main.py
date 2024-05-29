import telebot
import configbot_wi
import random
import pyowm
from pyowm import OWM
from pyowm.utils import config as cfg  # changes
from pyowm.utils import timestamps
from pyowm.commons import exceptions
from telebot import types

bot = telebot.TeleBot(configbot_wi.token)
user = bot.get_me()
updates = bot.get_updates()
# config = cfg.get_default_config()
# config['language'] = 'ru'
t = 0


@bot.message_handler(commands=['settings'])
def language(m):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("English", callback_data='UK')
    item2 = types.InlineKeyboardButton("Русский", callback_data='RF')
    markup.add(item1, item2)

    bot.send_message(m.chat.id, "Choose language:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def welcome(call):
    sti = open('/Users/kirillburtsev/Documents/sticker.webp', 'rb')
    bot.send_sticker(call.message.chat.id, sti)
    if call.message:
        if call.data == 'UK':
            bot.send_message(call.message.chat.id,
                             "Welcome! This bot was designed to get a weather forecast in any citys. \n Just send me the name of the city)")
        elif call.data == 'RF':
            bot.send_message(call.message.chat.id,
                             "Добро пожаловать! Бот показывает прогноз погоды для всех стран. \nПросто отправь мне название города)")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Language",
                              reply_markup=None)  # remove inline button

        # markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # item3 = types.KeyboardButton("")
        # item4 = types.KeyboardButton("")
        # markup.add(item3, item4)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Here are all available commands: \n /settings - change language")


@bot.message_handler(content_types=['text'])
def send_text(message):
    test = message.text.lower()
    owm = pyowm.OWM(configbot_wi.key)  # Захват города которий пишет человек
    test = message.text.lower()
    mgr = owm.weather_manager()

    try:  # Исключение
        observation = mgr.weather_at_place(test)
    except:
        bot.send_message(message.chat.id, 'Извините, произошла ошибка')

    w = observation.weather

    tempN = w.temperature('celsius')['temp']
    tempF = w.temperature('celsius')['feels_like']
    tempMAX = w.temperature('celsius')['temp_max']
    tempMIN = w.temperature('celsius')['temp_min']
    wind = w.wind()['speed']
    status = w.detailed_status
    humidity = w.humidity

    bot.send_message(message.chat.id,
                     f"It is {tempN}°C in {message.text}\nFeels like: {tempF}°C \nMax: {tempMAX}°C \nMin: {tempMIN}°C \nWind speed: {wind} m/s \nHumidity: {humidity}% \n{status}")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(message):
    bot.send_message(message.chat.id, "I don't understand \"" + message.text + "\"\nMaybe try the help page at /help")


bot.polling(none_stop=True)

