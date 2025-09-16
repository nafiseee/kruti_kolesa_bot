from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb,b_models,works_edit_kb,works_groups,return_works_kb,m_or_e_kb
from aiogram.fsm.context import FSMContext
from handlers.start import Form
from aiogram.types import FSInputFile
from create_bot import bot
from aiogram.utils.chat_action import ChatActionSender
from utils.info import info
from utils.dataframes import df
other  = Router()
audio_file = FSInputFile("media/1.mp3", "Сигма бой.mp3")
@other.message(F.text=='Отмена')
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Меню:',reply_markup=main_kb(message.from_user.id))
    await state.clear()
    await state.set_state(Form.client_start)

@other.message(F.text=='🎸 Музыка')
async def start_questionnaire_process(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer_audio(audio_file)