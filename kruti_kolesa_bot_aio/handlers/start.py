from aiogram import Router, F
import asyncio
from create_bot import bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile,ReplyKeyboardRemove,CallbackQuery
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb
from aiogram.utils.chat_action import ChatActionSender
from validators.validators import name_validate,phone_validate,act_validate,model_validate,id_validate,iot_validate,bycycle_type_validate,work_is_true
from datetime import timedelta
import pandas as pd
from utils.info import info
start_photo = FSInputFile('media/sticker.webm', filename='хуй')
client_work_keys = ['work_type','full_name','phone_number','act_id','b_model','b_id','iot_id']
client_work = ['','','Номер телефона: ','Акт №','Модель велосипеда: ','Номер велосипеда: ', 'IoT: ']


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


start  = Router()
questionnaire_router = Router()
works_router = Router()

df = pd.read_excel('works_norm.xlsx',names = ['work','time','type','sale','group'])
print(df)
async def init_work(state,message):
    print('ff')
    await state.update_data(works=[], user_id=message.from_user.id)
    await state.update_data(works_count={}, user_id=message.from_user.id)
    await state.update_data(sum_norm_time=0, user_id=message.from_user.id)
    await state.update_data(a=[], user_id=message.from_user.id)
    await state.update_data(norm_time=[], user_id=message.from_user.id)
    await state.update_data(spares=[], user_id=message.from_user.id)
    await state.update_data(spares_types=[], user_id=message.from_user.id)
    print('ff')
    print_data = await info(state)
    print(print_data)
    await message.answer(print_data, reply_markup=works_edit_kb())
    await state.set_state(Form.find_works)


@start.message(Command('start')) #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_photo(photo=FSInputFile('media/1.jpg', filename='Снеговик'),caption = 'Привет я твой помощник по занесению ремонтов. Что будем делать?', reply_markup=main_kb(message.from_user.id))
    await state.set_state(Form.client_start)

@start.message(F.text=='⚙️ Админ панель') #НАЧАЛО
async def start_questionnaire_process(message: Message, state: FSMContext):
    await bot.send_video(message.chat.id,open('media/prikol.mp4','rb'))

@questionnaire_router.message(F.text=='Техническое обслуживание',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time = (timedelta(hours=3)+message.date).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await message.answer('Введи номер акта: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)

@questionnaire_router.message(F.text=='Клиентский ремонт',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(work_type=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(start_time=(message.date+timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"))
        await state.update_data(employer=message.from_user.full_name)
        await state.update_data(message_id = message.from_user.id+1)
        await message.answer('Введи ФИО:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.full_name)

@questionnaire_router.message(F.text=='Аккомулятор',Form.client_start)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('папапам опаздываю на работу', reply_markup=ReplyKeyboardRemove())

@questionnaire_router.message(F.text,Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not name_validate(message.text):
        await message.reply("Пожалуйста, введите корректное ФИО в формате: Фамилия Имя:")
        return
    await state.update_data(full_name=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Введи номер телефона:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.phone_number)
@questionnaire_router.message(F.text,Form.phone_number)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not phone_validate(message.text):
        await message.reply("Пожалуйста введите номер в формате 8XXXXXXXXXX")
        return
    await state.update_data(phone_number=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Номер акта:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.act_id)
@questionnaire_router.message(F.text,Form.act_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not act_validate(message.text):
        await message.reply("Некоректный номер акта. Попробуйте еще раз")
        return
    await state.update_data(act_id=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Выберите тип велоиспеда:', reply_markup=m_or_e_kb())
    await state.set_state(Form.b_or_e)

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
@questionnaire_router.callback_query(F.data, Form.b_model)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    print(F.data)
    await state.update_data(b_model=call.data)
    print(call.message)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Номер велосипеда:')
    await state.set_state(Form.b_id)
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


@questionnaire_router.message(F.text,Form.iot_id)
async def start_questionnaire_process(message: Message, state: FSMContext):
    if not iot_validate(message.text):
        await message.reply("Некоректный номер IoT. Попробуйте еще раз")
        return
    await state.update_data(iot_id=message.text, user_id=message.from_user.id)
    await init_work(state,message)

# @questionnaire_router.message(F.text=="Добавить работу",Form.find_works)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     await message.reply("Выбери вид работы:",reply_markup=works_groups(await state.get_data(),df))
#     await state.set_state(Form.find_work)
#
# @questionnaire_router.message(F.text,Form.find_work)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     print(message.text)
#     print(df.group.unique())
#     if message.text in df.group.unique():
#         print('зашел')
#         await state.update_data(last_group=message.text)
#         await state.set_state(Form.add_work)
#         await message.reply("Выбери работу:",reply_markup=return_works_kb(await state.get_data(),df))
#     else:
#         await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(),df))
#         await state.set_state(Form.find_work)
#
# @questionnaire_router.message(F.text,Form.add_work)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     data = await state.get_data()
#     print(str(df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['work']))
#     print(message.text)
#     if message.text in df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['work'].unique():
#         data['works'].append(message.text)
#         data['norm_time'].append(float(
#             df.loc[((df['group']==data['last_group'])&
#                     (df['type']==data['m_or_e'])&
#                     (df['work']==message.text))]['time'].iloc[0]))
#         print(data['norm_time'],'==============================')
#         await state.update_data(data=data)
#         await state.set_state(Form.find_work)
#         # await message.reply(await info(state),reply_markup=works_groups(data,df))
#         print('DDD')
#         await message.answer(await info(state), reply_markup=works_edit_kb())
#     else:
#         await message.reply("Выбери вид работы:", reply_markup=works_groups(data,df))
#         await state.set_state(Form.find_work)
    # @questionnaire_router.message(F.text,Form.find_work)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     data = await state.get_data()
#     state.update_data(last_group = message.text)
#     await message.reply('Выбери работу',reply_markup=return_works_kb(message.text,data['m_or_e']))
#     await state.set_state(Form.add_work)
#
# @questionnaire_router.message(F.text,Form.add_work)
# async def start_questionnaire_process(message: Message, state: FSMContext):
#     data = await state.get_data()
#     print('автзтизутилутиутузитпузл')
#     works = data['works']
#     if work_is_true(message.text):
#         works.append(message.text)
#         state.update_data(works=works)
#         print_data = await info(state)
#         await message.reply(print_data,return_works_kb(message.text,data['m_or_e']))
#         await state.set_state(Form.find_work)
#     else:
#         await message.reply('Выбери работу', reply_markup=return_works_kb(message.text, data['m_or_e']))
#         await state.set_state(Form.add_work)

# @questionnaire_router.callback_query(F.data, Form.add_work)
# async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
#     if call.data =='Назад':
#         await call.message.reply("Выбери вид работы:", reply_markup=works_groups())
#         await state.set_state(Form.find_work)
#         return
#     data = await state.get_data()
#     works = data['works']
#     if not get_text(call.data) in works:
#         works.append(get_text(call.data))
#         await state.update_data(works=works)
#         sum_norm_time = data['sum_norm_time']
#         await state.update_data(sum_norm_time=sum_norm_time+norm_time[get_text(call.data)])
#         await state.set_state(Form.b_id)
#         data['works_count'][get_text(call.data)]=1
#     else:
#         data['works_count'][get_text(call.data)]+=1
#         await state.update_data(works_count = data['works_count'], user_id=call.message.from_user.id)
#         sum_norm_time = data['sum_norm_time']
#         await state.update_data(sum_norm_time=sum_norm_time + norm_time[get_text(call.data)])
#     print_data = await info(state)
#     await call.message.answer(print_data)
#     await call.message.answer("Выбери вид работы:", reply_markup=works_groups())
#     await state.set_state(Form.find_work)



