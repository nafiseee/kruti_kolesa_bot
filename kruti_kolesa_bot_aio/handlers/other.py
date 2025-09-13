from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb,spares_groups,return_spares_kb
from aiogram.fsm.context import FSMContext
from handlers.start import Form
from create_bot import bot
from utils.info import info
from utils.dataframes import df, df_spare
other  = Router()

@other.message(F.text=='Отмена')
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Меню:',reply_markup=main_kb(message.from_user.id))
    await state.clear()
    await state.set_state(Form.client_start)