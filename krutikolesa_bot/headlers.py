from telebot import types
from krutikolesa_bot.models import ClientWork
from models import Work,ClientWork
from keyboards import WORK_TYPE_BUTTON,BYCYCLE_MODEL_BUTTON,BACK_BUTTON
from validators import name_validate,phone_validate,act_validate,model_validate,id_validate,iot_validate
from pympler import tracker
works = {}
states = {}
from pympler import tracker

tr = tracker.SummaryTracker()
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
    works[message.from_user.id].print_params['client_name'] = '<b>Клиент: </b>'
def get_client_name(message,bot):
    print('ffff')
    works[message.from_user.id].client_name = message.text
    works[message.from_user.id].print_params['client_phone'] =  '\n<b>Номер телефона: </b>'
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_client_phone'
def get_client_phone(message,bot):
    works[message.from_user.id].client_phone = message.text
    works[message.from_user.id].print_params['act'] = '\n<b>Номер акта: </b>'
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_act'

def get_act(message,bot):
    works[message.from_user.id].act = message.text
    works[message.from_user.id].print_params['bycycle_model'] =  '\n<b>Модель велосипеда: </b>'
    bot.send_message(message.from_user.id, works[message.from_user.id].info(), reply_markup=BYCYCLE_MODEL_BUTTON, parse_mode="html")
    states[message.from_user.id] = 'getting_bycycle_model'
def get_bycycle_model(message,bot):
    print('Хуй')
    works[message.from_user.id].bycycle_model  = message.text
    works[message.from_user.id].print_params['bycycle_id'] =  '\n<b>Номер велосипеда: </b>'
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_bycycle_id'
def get_bycyle_id(message,bot):
    works[message.from_user.id].bycycle_id = message.text
    works[message.from_user.id].print_params['iot_id'] =  '\n<b>Номер iot модуля: </b>'
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getting_iot'
    print('f'*100)
def get_iot(message,bot):
    works[message.from_user.id].iot_id = message.text
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html",reply_markup=BACK_BUTTON)
    states[message.from_user.id] = 'getted_info'
def headler(message,bot):

    if message.text=='/start' or message.text in ['Назад','В начало']:
        main(message,bot)
    elif message.text == 'Начать ремонт👰🏼':
        get_start(message,bot)
    elif message.text == 'Клиентский ремонт':
        get_work_type(message,bot)
    elif states[message.from_user.id] == 'getting_client_name':
        if name_validate(message):
            get_client_name(message,bot)
        else:
            get_work_type(message,bot)
    elif states[message.from_user.id] == 'getting_client_phone':
        if phone_validate(message):
            get_client_phone(message,bot)
        else:
            get_client_name(message,bot)
    elif states[message.from_user.id] == 'getting_act':
        if act_validate(message):
            get_act(message,bot)
        else:
            get_client_phone(message,bot)
    elif states[message.from_user.id] == 'getting_bycycle_model':
        if model_validate(message):
            get_bycycle_model(message,bot)
        else:
            get_act(message,bot)
    elif states[message.from_user.id] == 'getting_bycycle_id':
        if id_validate(message):
            get_bycyle_id(message,bot)
        else:
            get_bycycle_model(message,bot)
    elif states[message.from_user.id] == 'getting_iot':
        if iot_validate(message):
            get_iot(message,bot)
        else:
            get_bycyle_id(message,bot)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    tr.print_diff()



    print(states)

