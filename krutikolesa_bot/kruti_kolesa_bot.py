import telebot
from telebot import types


works ={}
class Work():
    def __init__(self,worker_id,worker_name):
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.act = ''
        self.bycycle_model = ''
        self.bycycle_id = ''
        self.bycycle_state_id = ''
        self.iot_id = ''

        self.works = []
        self.spare_parts = []
        self.status = 'Ремонт не окончен'
        self.print_params = []
    def __str__(self):
        print('fdfdfddfdfffffffffffffffff')
        return str(dir(self))


class ClientWork(Work):
    def __init__(self,worker_id,worker_name):
        super().__init__(worker_id,worker_name)
        self.client_name = ''
        self.client_phone = ''
    def info(self):
        print(self.print_params)
        s = "-----------------------------\nКлиентский ремонт\n"
        for i in self.print_params:
            s+=i[1]
            print(s)
            if getattr(self, i[0]):
                s+=getattr(self, i[0])
            else:
                s+=' ____\n'
        return s



employers = [933028899,1003927607]


bot = telebot.TeleBot('8333772503:AAGK6KQl9b0J9727WzfokrUPq5QxBcbJdFs')
states = {}
for i in employers:
    states[i] = 'none'




def main(message):

    main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_repair = types.KeyboardButton("Начать ремонт👰🏼")
    button2 = types.KeyboardButton("❓ Задать вопрос")
    main.add(start_repair, button2)
    bot.send_message(message.from_user.id, "Что будем делать?", reply_markup=main)
    message_id = message.id
    print(message_id)

@bot.message_handler(func=lambda message: message.text == 'Начать ремонт👰🏼')
def get_work_type(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id-1)
    bot.delete_message(message.chat.id, message.message_id-2)
    states[message.from_user.id] = 'getting_type'
    main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_repair = types.KeyboardButton("Клиентский ремонт")
    button2 = types.KeyboardButton("Тех обслуживание")
    main.add(start_repair, button2)
    bot.send_message(message.from_user.id, "Тип ремонта:", reply_markup=main)



@bot.message_handler(func=lambda message: message.text == 'Клиентский ремонт')
def get_work_type(message):
    bot.send_message(message.from_user.id, "Имя и фамилия клиента")
    states[message.from_user.id] = 'getting_client_name'
    works[message.from_user.id] = ClientWork(message.from_user.id,f"{message.from_user.first_name} {message.from_user.first_name}")
    works[message.from_user.id].print_params.append(['client_name','<b>Клиент: </b>'])


@bot.message_handler(func=lambda message: states[message.from_user.id] == 'getting_client_name')
def getting_client_name(message):
    print('ffff')
    works[message.from_user.id].client_name = message.text
    works[message.from_user.id].print_params.append(['client_phone', '\n<b>Номер телефона: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html")
    states[message.from_user.id] = 'getting_client_phone'


@bot.message_handler(func=lambda message: states[message.from_user.id] == 'getting_client_phone')
def getting_client_name(message):
    works[message.from_user.id].client_phone = message.text
    works[message.from_user.id].print_params.append(['act', '\n<b>Номер акта: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html")
    states[message.from_user.id] = 'getting_client_act'

@bot.message_handler(func=lambda message: states[message.from_user.id] == 'getting_client_act')
def getting_client_name(message):
    works[message.from_user.id].act = message.text
    works[message.from_user.id].print_params.append(['bycycle_model', '\n<b>Модель велосипеда: </b>'])

    main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ms15 = types.KeyboardButton("Шаркусь монстр 15")
    ms20 = types.KeyboardButton("Шаркусь монстр 20")
    mm15 = types.KeyboardButton("Мингто монстр 15")
    mpro = types.KeyboardButton("Монстр про")
    kr15 = types.KeyboardButton("Крути 15")
    main.add(ms15, ms20, mm15, mpro, kr15)

    bot.send_message(message.from_user.id, works[message.from_user.id].info(),reply_markup=main,parse_mode="html")
    states[message.from_user.id] = 'getting_bycycle_model'

@bot.message_handler(func=lambda message: states[message.from_user.id] == 'getting_bycycle_model')
def getting_client_name(message):
    print('Хуй')
    works[message.from_user.id].bycycle_model  = message.text
    works[message.from_user.id].print_params.append(['bycycle_id', '\n<b>Номер велосипеда: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html")
    states[message.from_user.id] = 'getting_bycycle_id'

@bot.message_handler(func=lambda message: states[message.from_user.id] == 'getting_bycycle_id')
def getting_client_name(message):
    works[message.from_user.id].bycycle_id = message.text
    works[message.from_user.id].print_params.append(['iot_id', '\n<b>Номер iot модуля: </b>'])
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html")
    states[message.from_user.id] = 'getting_iot'

@bot.message_handler(func=lambda message: states[message.from_user.id] == 'getting_iot')
def getting_client_name(message):
    works[message.from_user.id].iot_id = message.text
    bot.send_message(message.from_user.id, works[message.from_user.id].info(),parse_mode="html")
    states[message.from_user.id] = 'none'


@bot.message_handler(content_types=['text'])
def auth(message):
    if message.from_user.id in employers:
        states[message.from_user.id] = 'none'
        print('ffffffff')
        bot.send_message(message.from_user.id, "Приветик")
        main(message)
    else:
        bot.send_message(message.from_user.id, "Тебя нет в нашей дружной команде КрутиКолеса🥰")

    # print('вызов')
    #
    #     print(message.text)
    #     if message.text == '/start':
    #
    #
    #         main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #         start_repair = types.KeyboardButton("Начать ремонт👰🏼")
    #         button2 = types.KeyboardButton("❓ Задать вопрос")
    #         main.add(start_repair, button2)
    #         bot.send_message(message.from_user.id, "Приветик", reply_markup=main)
    #
    #     elif message.text == 'Начать ремонт👰🏼':
    #         main = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #         b1 = types.KeyboardButton("Модель")
    #         b2 = types.KeyboardButton("Номер велика")
    #         b3 = types.KeyboardButton("гос номер")
    #         b4 = types.KeyboardButton("iot")
    #         main.add(b1,b2,b3,b4)
    #         bot.send_message(message.from_user.id, "Ремонт", reply_markup=main)
    #         work = Work(message.from_user.id,message.from_user.first_name)
    #         print(work)
    #
    #     else:
    #         bot.send_message(message.from_user.id, "Что будем делать?",reply_markup=main)









bot.polling(none_stop=True)