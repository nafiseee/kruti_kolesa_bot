from telebot import types

BYCYCLE_MODEL_BUTTON = types.ReplyKeyboardMarkup(resize_keyboard=True)
ms15 = types.KeyboardButton("Шаркусь монстр 15")
ms20 = types.KeyboardButton("Шаркусь монстр 20")
mm15 = types.KeyboardButton("Мингто монстр 15")
mpro = types.KeyboardButton("Монстр про")
kr15 = types.KeyboardButton("Крути 15")
BYCYCLE_MODEL_BUTTON.add(ms15, ms20, mm15, mpro, kr15)


WORK_TYPE_BUTTON = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_repair = types.KeyboardButton("Клиентский ремонт")
button2 = types.KeyboardButton("Тех обслуживание")
WORK_TYPE_BUTTON.add(start_repair, button2)

BACK_BUTTON = types.ReplyKeyboardMarkup(resize_keyboard=True)
start_repair = types.KeyboardButton("Назад")
BACK_BUTTON.add(start_repair)