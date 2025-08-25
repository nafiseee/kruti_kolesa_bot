import telebot
from config import TOKEN,USERS
from krutikolesa_bot.headlers import headler



bot = telebot.TeleBot(TOKEN)

users = {}




@bot.message_handler(content_types=['text'])
def main_headler(message):
    if message.from_user.id in USERS:
        headler(message,bot)



if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
