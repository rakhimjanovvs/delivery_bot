import telebot
import buttons
import config
import database

# Создаем объект бота
bot = telebot.TeleBot(config.TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # проверяем юзера на наличие в БД
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию! Напишите свое имя', reply_markup=telebot.types.ReplyKeyboardRemove())

        # Переход на этап получение имени
        bot.register_next_step_handler(message, get_name)

# Этап получение имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер!', reply_markup=buttons.num_button())
    # Переход на этап получение номера
    bot.register_next_step_handler(message, get_num, user_name)

# Этап получение номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # проверка на правильность номера
    if message.contact:
        user_num = message.contact.phone_number
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!', reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!')
        # Возврашаем на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)

# Запуск бота
bot.polling(non_stop=True)