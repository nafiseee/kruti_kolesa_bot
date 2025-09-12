from aiogram import Router, F
import asyncio
from create_bot import bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile,ReplyKeyboardRemove,CallbackQuery
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb,spares_groups,return_spares_kb
from aiogram.utils.chat_action import ChatActionSender
from validators.validators import name_validate,phone_validate,act_validate,model_validate,id_validate,iot_validate,bycycle_type_validate,work_is_true
import pandas as pd
start_photo = FSInputFile('media/sticker.webm', filename='хуй')
prikol = FSInputFile('media/prikol.mp4', filename='хуй')
client_work_keys = ['work_type','full_name','phone_number','act_id','b_model','b_id','iot_id']
client_work = ['','','Номер телефона: ','Акт №','Модель велосипеда: ','Номер велосипеда: ', 'IoT: ']
async def info(state):
    data = await state.get_data()
    s = f"<b>Мастер:</b> {data['employer']} | {data['start_time']}\n\n"
    for q,w in enumerate(client_work_keys):
        if w in data:
            if client_work[q]:
                s+=f"<b>{client_work[q]}</b> {data[w]}\n"
            else:
                s+=f"<b>{data[w]}\n</b>"
    s+='\n<b>Выполненные работы:</b>\n'
    if data['works']==[]:
        for i in range(3):
            print('fdddddddddddddddddddd')
            s+='____________\n'
    else:
        for i in data['works']:
            if i not in data['works_count']:
                s+=f"{i}\n"
            else:
                if data['works_count'][i]==1:
                    s += f"{i}\n"
                else:
                    s += f"{i} ({data['works_count'][i]}x)\n"
    s+="\n<b>Запчасти:</b>\n"
    if data['spares']==[]:
        for i in range(3):
            print('fdddddddddddddddddddd')
            s+='____________\n'
        else:
            for i in data['spares']:
                if i not in data['works_count']:
                    s += f"{i}\n"
                else:
                    if data['works_count'][i] == 1:
                        s += f"{i}\n"
                    else:
                        s += f"{i} ({data['works_count'][i]}x)\n"

    else:
        for i in data['spares']:
            s+=f"{i}\n"
    s+=f"\n<b>Норма часы:</b> {sum(data['norm_time'])}👺"
    return s

class Form(StatesGroup):
    client_start = State()
    full_name = State()
    phone_number = State()
    act_id = State()
    b_or_e = State()
    b_model = State()
    b_id = State()
    iot_id = State()
    find_works = State()
    find_work = State()
    add_work  = State()
    find_spare = State()
    add_spare = State()
    find_spares = State()
    wait = State()
start  = Router()
questionnaire_router = Router()

df = pd.read_excel('works_norm.xlsx',names = ['work','time','type','sale','group'])
df_spare = pd.read_excel('spares.xlsx',names = ['spare','type','group'])
async def init_work(state,message):
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    print_data = await info(state)
    await message.answer(print_data, reply_markup=works_edit_kb())
    await state.set_state(Form.wait)

#НАЧАЛО
@start.message(Command('start'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),caption = 'Привет я твой помощник по занесению ремонтов. Что будем делать?', reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)
#АДМИН ПАНЕЛЬ
@start.message(F.text=='⚙️ Админ панель') #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer_video(prikol)
#ТО
@questionnaire_router.message(F.text=='Техническое обслуживание',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time = message.date.strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await message.answer('Введи номер акта: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)
#КЛИЕНТСКИЙ РЕМОНТ
@questionnaire_router.message(F.text=='Клиентский ремонт',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time=message.date.strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await state.update_data(message_id = message.from_user.id+1)
        await message.answer('Введи ФИО:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.full_name)
#ФИО
@questionnaire_router.message(F.text,Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not name_validate(message.text):
        await message.reply("Пожалуйста, введите корректное ФИО в формате Иванов Иван Иванович:")
        return
    await state.update_data(full_name=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Введи номер телефона:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.phone_number)
#НОМЕР ТЕЛЕФОНА
@questionnaire_router.message(F.text,Form.phone_number)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not phone_validate(message.text):
        await message.reply("Пожалуйста введите номер в формате 8XXXXXXXXXX")
        return
    await state.update_data(phone_number=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Номер акта:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)
#НОМЕР АКТА
@questionnaire_router.message(F.text,Form.act_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not act_validate(message.text):
        await message.reply("Некоректный номер акта. Попробуйте еще раз")
        return
    await state.update_data(act_id=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите тип велоиспеда:', reply_markup=m_or_e_kb())
    await state.set_state(Form.b_or_e)
#МЕХАНИКА ИЛИ ЭЛЕКТРО
@questionnaire_router.message(F.text,Form.b_or_e)
async def start_questionnaire_process(message: Message, state: FSMContext):

    if not bycycle_type_validate(message.text):
        await message.reply("Некоректный тип велосипеда. Попробуйте заново",reply_markup=m_or_e_kb())
        return

    await state.update_data(m_or_e=message.text, user_id=message.from_user.id)
    data = await state.get_data()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите модель велосипеда:', reply_markup=b_models(data['m_or_e']))
    await state.set_state(Form.b_model)
#МОДЕЛЬ ВЕЛИКА
@questionnaire_router.message(F.text,Form.b_model)
async def start_questionnaire_process(message: Message, state: FSMContext):
    data = await state.get_data()
    if not model_validate(message.text):
        await message.reply("Выберите модель из списка:",reply_markup=b_models(data['m_or_e']))
        return
    # await message.reply("вывыыввыыв")
    # await state.update_data(b_model=message.text, user_id=message.from_user.id)
    # async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
    #     await message.answer('Номер акта:', reply_markup=ReplyKeyboardRemove())
    # await state.set_state(Form.act_id)
#МОДЕЛЬ ВЕЛИКА ФОРМА
@questionnaire_router.callback_query(F.data, Form.b_model)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await state.update_data(b_model=call.data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Номер велосипеда:')
    await state.set_state(Form.b_id)
#НОМЕР ВЕЛОСИПЕДА
@questionnaire_router.message(F.text,Form.b_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not id_validate(message.text):
        await message.reply("Некоректный номер велика. Попробуйте еще раз")
        return
    await state.update_data(b_id=message.text, user_id=message.from_user.id)
    if await state.get_value('m_or_e') != 'Механика':
        await message.answer('Введите номер IoT модуля:', reply_markup=None)
        await state.set_state(Form.iot_id)
    else:
        await init_work(state,message)
#НОМЕР IOT
@questionnaire_router.message(F.text,Form.iot_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not iot_validate(message.text):
        await message.reply("Некоректный номер IoT. Попробуйте еще раз")
        return
    await state.update_data(iot_id=message.text, user_id=message.from_user.id)
    await init_work(state,message)






#=======================================================================================================



