import telebot
import random
from telebot import types
bot = telebot.TeleBot('')
@bot.message_handler(commands=['start'])
def start(message):
    text = f'<b>Привет! {message.from_user.first_name} я бот для генерации паролей, для начала напиши комманду /createpass</b>'
    bot.send_message(message.chat.id, text, parse_mode='html')
@bot.message_handler(commands=['createpass'])
def createpass(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button_exit =types.KeyboardButton("Выход")
    keyboard.add(button_exit)
    msg = bot.send_message(message.chat.id, 'Введите кол-во символов для пароля:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_choice)
def generate_password(message):
    length = int(message.text)
    password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button_good = types.KeyboardButton(text='Спасибо')
    button_another = types.KeyboardButton(text='Еще вариант')
    button_exit =types.KeyboardButton("Выход")
        
    keyboard.add(button_good, button_another, button_exit)
    msg = bot.send_message(message.chat.id, f'Сгенерированный пароль: {password}', reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_choice)

    def handle_choice(message):
     if message.text.isnumeric():
        generate_password(message)
     elif message.text == 'Спасибо':
        bot.send_message(message.chat.id, 'Незачто я всего бот!)')
        start(message)
     elif message.text == 'Еще вариант':
        msg = bot.send_message(message.chat.id, 'Введите, какой длины нужен новый пароль:')
        bot.register_next_step_handler(msg, generate_password)
     elif message.text=="Выход":
        start(message)
        bot.polling()