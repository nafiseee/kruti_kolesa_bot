from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb, b_models, works_edit_kb, works_groups, return_works_kb, m_or_e_kb,add_spares,spares_list_for_work,return_spares_group,return_spares
from aiogram.fsm.context import FSMContext
import pandas as pd
from utils.info import info
from utils.dataframes import df,df_spares


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
    find_spare_ = State()
    add_spare = State()
    add_spare_ = State()
    find_spares = State()
    wait = State()
    getting_spare = State()
    getting_spare_ = State()
    next_menu = State()
spares_router = Router()


@spares_router.message(F.text=='➕ Добавить запчасть',Form.next_menu)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(1)
    await state.set_state(Form.getting_spare_)
    await message.answer("Введи зч", reply_markup=spares_list_for_work())
@spares_router.message(F.text.contains("Запчасти не использовались"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(2)
    await state.set_state(Form.next_menu)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())
@spares_router.message(F.text,Form.getting_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(3)
    data = await state.get_data()
    if 'б/у' in message.text:
        data['spares_types'].append('б/у')
        print("он выбрал бу")
    else:
        data['spares_types'].append('')
        print("он выбрал НЕ бу")
    await message.reply("Выбери группу запчастей:", reply_markup=return_spares_group(df_spares, await state.get_data()))
    await state.set_state(Form.find_spare_)
@spares_router.message(F.text,Form.find_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(4)
    data = await state.get_data()
    if message.text == 'Назад':
        await state.set_state(Form.client_start)
        await message.answer('хих', reply_markup=works_edit_kb())
        return
    print(message.text)
    print('хуй', df_spares[df_spares['type'] == data['m_or_e']].group.unique())
    if message.text in df_spares[df_spares['type'] == data['m_or_e']].group.unique():
        print('правильно же сука')
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.reply("Выбери запчасть:", reply_markup=return_spares(df_spares, await state.get_data()))
    else:
        await message.reply("Выбери группу запчастей:",
                            reply_markup=return_spares_group(df_spares, await state.get_data()))
        await state.set_state(Form.find_spare)
@spares_router.message(F.text,Form.add_spare_)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(7)
    data = await state.get_data()
    v_spares = df_spares.loc[((df_spares['group'] == data['last_spare_group']) & (df_spares['type'] == data['m_or_e']))]['spares'].unique()
    print(message.text,v_spares)
    if message.text in v_spares:
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await message.answer(await(info(state)),reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
@spares_router.message(F.text,Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(5)
    data = await state.get_data()
    if message.text=='Назад':
        await state.set_state(Form.client_start)
        await message.answer('хих',reply_markup=works_edit_kb())
        return
    print(message.text)
    print('хуй',df_spares[df_spares['type'] == data['m_or_e']].group.unique())
    if message.text in df_spares[df_spares['type']==data['m_or_e']].group.unique():
        print('правильно же сука')
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare_)
        await message.reply("Выбери запчасть:",reply_markup=return_spares(df_spares,await state.get_data()))
    else:
        await message.reply("Выбери группу запчастей:",
                            reply_markup=return_spares_group(df_spares, await state.get_data()))
        await state.set_state(Form.find_spare)
#=======================================================================================================================
@spares_router.message(F.text,Form.getting_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(8)
    data = await state.get_data()
    v_spares = df[df['works']==data['works'][-1]]['spares'].unique()
    if 'б/у' in message.text:
        data['spares_types'].append('б/у')
    else:
        data['spares_types'].append('')
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_spare)
    await state.update_data(spares_variant=v_spares)
@spares_router.message(F.text,Form.add_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print(6)
    data = await state.get_data()
    print('тута')
    if message.text in list(data['spares_variant']):
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await message.answer(await info(state), reply_markup=works_edit_kb())
        await state.set_state(Form.next_menu)
        print('nenf')
    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
        await state.set_state(Form.find_spare)