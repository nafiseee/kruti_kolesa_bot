from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb,add_spares,spares_list_for_work
from aiogram.fsm.context import FSMContext
import pandas as pd
from utils.info import info
from utils.dataframes import df
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
    add_work = State()
    find_spare = State()
    add_spare = State()
    find_spares = State()
    wait = State()
    getting_spare = State()

works_router = Router()

@works_router.message(F.text == "Добавить работу")
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('выюбор группы рабюот')
    await state.set_state(Form.find_work)
    await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(), df))
    await state.set_state(Form.find_work)

@works_router.message(F.text,Form.find_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('выбор работ')
    if message.text=='Назад':
        await state.set_state(Form.client_start)
        await message.answer('хих',reply_markup=works_edit_kb())
        return
    if message.text in df[df['type']==await state.get_value('m_or_e')].group.unique():
        await state.update_data(last_group=message.text)
        await state.set_state(Form.add_work)
        await message.reply("Выбери работу:",reply_markup=return_works_kb(await state.get_data(),df))
    else:
        await message.reply("Выбери вид работы:", reply_markup=works_groups(await state.get_data(),df))
        await state.set_state(Form.find_work)
#ДОБАВЛЕНИЕ РАБОТЫ
@works_router.message(F.text,Form.add_work)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('добавление работы')
    data = await state.get_data()
    if message.text in df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['works'].unique():
        data['works'].append(message.text)
        data['norm_time'].append(float(
            df.loc[((df['group']==data['last_group'])&
                    (df['type']==data['m_or_e'])&
                    (df['works']==message.text))]['time'].iloc[0]))
        await state.update_data(data=data)
        await state.set_state(Form.getting_spare)
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
    else:
        await message.reply("Выбери вид работы:", reply_markup=works_groups(data,df))
        await state.set_state(Form.find_work)

