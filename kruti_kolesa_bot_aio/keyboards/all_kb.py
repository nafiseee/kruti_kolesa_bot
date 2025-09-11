from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from electro_works import electro_works
from mechanical_works import mechanical_works



def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="Клиентский ремонт"), KeyboardButton(text="Техническое обслуживание")],
        [KeyboardButton(text="Сделать чета"), KeyboardButton(text="Еще чета")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def m_or_e_kb():
    kb_list = [
        [KeyboardButton(text="Механика")],
        [KeyboardButton(text="Электро")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
def works_edit_kb():
    kb_list = [
        [KeyboardButton(text="Добавить работу"), KeyboardButton(text="Добавить ЗЧ")],
        [KeyboardButton(text="сегодня какал сильно тужилсяяя"), KeyboardButton(text="пупупууум")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def b_models(a):
    kb_list = [
        [InlineKeyboardButton(text="Шаркусь монстр 15", callback_data='Шаркусь монстр 15')],
        [InlineKeyboardButton(text="Шаркусь монстр 20", callback_data='Шаркусь монстр 20')],
        [InlineKeyboardButton(text="Мингто монстр 20", callback_data='Мингто монстр 20')],
        [InlineKeyboardButton(text="Монстр про", callback_data='Монстр про')],
        [InlineKeyboardButton(text="Крути 15", callback_data='Крути 15')]]
    kb_list2 = [[InlineKeyboardButton(text="Forward 27.5", callback_data='Forward 27.5')],
                [InlineKeyboardButton(text="Forward 29", callback_data='Forward 29')],
                [InlineKeyboardButton(text="Kruti 27.5", callback_data='Kruti 27.5')],
                [InlineKeyboardButton(text="Kruti 29", callback_data='Kruti 29')]
                ]
    if a=='Механика':
        return InlineKeyboardMarkup(inline_keyboard=kb_list2)
    else:
        return InlineKeyboardMarkup(inline_keyboard=kb_list)
#dict_keys(['accumulator', 'electronics', 'braking_system', 'drive_train', 'frame_and_wheels', 'body_and_cosmetic', 'lighting', 'other'])
def works_groups(data,df):
    kb = [[KeyboardButton(text=i)] for i in df[df['type']==data['m_or_e']]['group'].unique()]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


q_e = {
    "Рама и вилка": "frame_and_fork",
    "Колеса и шины": "wheels_and_tires",
    "Тормозная система": "brake_system",
    "Трансмиссия": "transmission",
    "Рулевое управление": "steering_control",
    "Электроника": "electronics",
    "Аккумуляторная система": "battery_system",
    "Освещение и сигнализация": "lighting_and_signaling",
    "Дисплей и управление": "display_and_control",
    "Сиденье и подседельная система": "seat_and_seatpost_system",
    "Крылья и защита": "fenders_and_protection",
    "Подножки и багажник": "footrests_and_luggage_rack",
    "IOT модули": "iot_modules",
    "Техническое обслуживание": "technical_maintenance",
    "PRO серия": "pro_series",
    "Сборка/разборка": "assembly_disassembly",
    "Прочее": "other"
}
q_inv = {v: k for k, v in q_e.items()}
print(q_inv)
def return_works_kb(data,df):
    kb = [[KeyboardButton(text=i)] for i in df.loc[((df['group']==data['last_group'])&(df['type']==data['m_or_e']))]['work']]
    keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:"
        )
    return keyboard
    # for i in grouped[q[a]]:
    #     kb_list.append([InlineKeyboardButton(text=i, callback_data=f"{q[a]}|{str(n)}")])
    #     n+=1
    # kb_list.append([InlineKeyboardButton(text='Назад', callback_data="Назад")])
    # return InlineKeyboardMarkup(inline_keyboard=kb_list)

def get_text(a):
    qq = a.split('|')
    return grouped[qq[0]][int(qq[1])]
def get_norm_time(a):
    qq = a.split('|')
    return