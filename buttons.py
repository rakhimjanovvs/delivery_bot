from telebot import types

# Кнопка отправки номера
def num_button():
    # Создание пространства
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Содание кнопок
    but1 = types.KeyboardButton('Отправить номер📞', request_contact=True)
    # Добавление кнопок в пространство
    kb.add(but1)
    return kb