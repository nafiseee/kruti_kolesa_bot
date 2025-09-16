from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb, b_models, works_edit_kb, works_groups, return_works_kb, m_or_e_kb,add_spares,spares_list_for_work
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

spares_router = Router()




@spares_router.message(F.text,Form.add_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text in list(data['spares_variant']):
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await message.answer(await(info(state)),reply_markup=works_edit_kb())
    else:
        await message.answer("Введи зч", reply_markup=spares_list_for_work())
@spares_router.message(F.text.contains("Запчасти не использовались"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.set_state(Form.add_spare)
    await message.answer(await(info(state)), reply_markup=works_edit_kb())
@spares_router.message(F.text.contains("Добавить ЗЧ"))
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('аазввахавььвах')
    data = await state.get_data()
    # df.loc[(df['works'] > 1) & (df['shield'] < 8)]
    v_spares = df[df['works']==data['works'][-1]]['spares'].unique()

    if 'б/у' in message.text:
        data['spares_types'].append('б/у')
    else:
        data['spares_types'].append('')
    await message.reply("Запчасти:", reply_markup=add_spares(v_spares))
    await state.set_state(Form.add_spare)
    await state.update_data(spares_variant=v_spares)

@spares_router.message(F.text,Form.find_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('выбор запчасти')
    if message.text=='Назад':
        await state.set_state(Form.client_start)
        await message.answer('хих',reply_markup=works_edit_kb())
        return
    if message.text in df_spare.group.unique():
        await state.update_data(last_spare_group=message.text)
        await state.set_state(Form.add_spare)
        await message.reply("Выбери запчасть:",reply_markup=return_spares_kb(await state.get_data(),df_spare))
    else:
        await message.reply("Выбери группу запчастей:", reply_markup=spares_groups(await state.get_data(),df_spare))
        await state.set_state(Form.find_spare)
#ДОБАВЛЕНИЕ РАБОТЫ
@spares_router.message(F.text,Form.add_spare)
async def start_questionnaire_process(message: Message, state: FSMContext):
    print('добавление зч')
    data = await state.get_data()
    if message.text in df_spare.loc[((df_spare['group']==data['last_spare_group'])&(df_spare['type']==data['m_or_e']))]['spare'].unique():
        data['spares'].append(message.text)
        await state.update_data(data=data)
        await state.set_state(Form.wait)
        await message.answer(await info(state), reply_markup=works_edit_kb())

    else:
        await message.reply("Выбери группу запчастей:", reply_markup=spares_groups(data,df_spare))
        await state.set_state(Form.find_spare)