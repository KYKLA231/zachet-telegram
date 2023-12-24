import random
import string
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

LENGTH, CHOICE = range(2)

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот-генератор паролей. Введите /password, чтобы начать генерацию пароля.")

def password_start(update, context):
    reply_keyboard = [['Хорошо', 'Еще вариант']]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите длину пароля:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return LENGTH

def password_length(update, context):
    length = int(update.message.text)
    password = generate_password(length)
    context.user_data['password'] = password
    reply_keyboard = [['Хорошо', 'Еще вариант']]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваш пароль: {password}", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CHOICE

def password_choice(update, context):
    choice = update.message.text
    if choice == 'Хорошо':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Отлично! Если вам нужен еще пароль, введите /password.")
        return ConversationHandler.END
    elif choice == 'Еще вариант':
        return password_start(update, context)

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Генерация пароля отменена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Список доступных команд:\n"
                                                                    "/start - начать генерацию пароля\n"
                                                                    "/help - получить список команд\n"
                                                                    "/password - сгенерировать новый пароль")

def main():
    updater = Updater(token='6963485677:AAFr8oKrp3MdUgDjVxQgfEmlFZJqdVFuiVg', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    password_handler = ConversationHandler(
        entry_points=[CommandHandler('password', password_start)],
        states={
            LENGTH: [MessageHandler(Filters.text, password_length)],
            CHOICE: [MessageHandler(Filters.text, password_choice)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    help_handler = CommandHandler('help', help_command)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(password_handler)
    dispatcher.add_handler(help_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
