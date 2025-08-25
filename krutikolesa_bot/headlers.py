from telebot import types
from krutikolesa_bot.models import ClientWork
from models import Work,ClientWork
from keyboards import WORK_TYPE_BUTTON,BYCYCLE_MODEL_BUTTON,BACK_BUTTON
works = {}
states = {}
print('ffffffffffffffffffffff')
def main(message,bot):

    main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_repair = types.KeyboardButton("Начать ремонт👰🏼")
    button2 = types.KeyboardButton("❓ Задать вопрос")
    main.add(start_repair, button2)
    bot.send_message(message.from_user.id, "Что будем делать?", reply_markup=main)
    message_id = message.id
    print(message_id)
def get_start(message,bot):
    print(message.from_user.id)
    if message.from_user.id not in states:
        states[message.from_user.id] = 'none'
    print(message)
    states[message.from_user.id] = 'getting_type'
    bot.send_message(message.from_user.id, "Тип ремонта:", reply_markup=WORK_TYPE_BUTTON)
def get_work_type(message,bot):
    bot.send_message(message.from_user.id, "Имя и фамилия клиента",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_client_name'
    works[message.from_user.id] = ClientWork(message.from_user.id,f"{message.from_user.first_name} {message.from_user.first_name}")
    works[message.from_user.id].print_params.append(['client_name','<b>Клиент: </b>'])
def get_client_name(message,bot):
    print('ffff')
    works[message.from_user.id].client_name = message.text
    works[message.from_user.id].print_params.append(['client_phone', '\n<b>Номер телефона: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_client_phone'
def get_client_phone(message,bot):
    works[message.from_user.id].client_phone = message.text
    works[message.from_user.id].print_params.append(['act', '\n<b>Номер акта: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_act'

def get_act(message,bot):
    works[message.from_user.id].act = message.text
    works[message.from_user.id].print_params.append(['bycycle_model', '\n<b>Модель велосипеда: </b>'])


    bot.send_message(message.from_user.id, works[message.from_user.id].info(), reply_markup=BYCYCLE_MODEL_BUTTON, parse_mode="html")
    states[message.from_user.id] = 'getting_bycycle_model'
def get_bycycle_model(message,bot):
    print('Хуй')
    works[message.from_user.id].bycycle_model  = message.text
    works[message.from_user.id].print_params.append(['bycycle_id', '\n<b>Номер велосипеда: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_bycycle_id'
def get_bycyle_id(message,bot):
    works[message.from_user.id].bycycle_id = message.text
    works[message.from_user.id].print_params.append(['iot_id', '\n<b>Номер iot модуля: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_iot'
def get_iot(message,bot):
    works[message.from_user.id].iot_id = message.text
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getted_info'
def headler(message,bot):
    if message.text=='/start' or message.text=='Назад':
        main(message,bot)
    elif message.text == 'Начать ремонт👰🏼':
        get_start(message,bot)
    elif message.text == 'Клиентский ремонт':
        get_work_type(message,bot)
    elif states[message.from_user.id] == 'getting_client_name':
        get_client_name(message,bot)
    elif states[message.from_user.id] == 'getting_client_phone':
        get_client_phone(message,bot)
    elif states[message.from_user.id] == 'getting_act':
        get_act(message,bot)
    elif states[message.from_user.id] == 'getting_bycycle_model':
        get_bycycle_model(message,bot)
    elif states[message.from_user.id] == 'getting_bycycle_id':
        get_bycyle_id(message,bot)
    elif states[message.from_user.id] == 'getting_iot':
        get_iot(message,bot)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)




    print(states)

