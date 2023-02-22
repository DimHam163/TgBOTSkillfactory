import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ConverterCurrency
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     f'Добро пожаловать ✋🏼 {message.chat.username}')  # выводим приветственное сообщение
    bot.send_animation(message.chat.id,
                       r'https://media.tenor.com/nJDAgh_80UMAAAAj/nabung-investasi.gif')  # добавим ГИфку)
    bot.send_message(message.from_user.id, 'Чтобы подробно узнать о функционале данного бота, необходимо '
                                           'воспользоваться ➡️/help  | Поддержка - /setting')
    pass


@bot.message_handler(commands=['setting'])  # обавим "не менюшную" кнопку специально для Skillfactory )
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Жми кнопку',
                                      url='https://skillfactory.ru/')  # чисто по ФАНУ))
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Skillfactory ⤵", reply_markup=markup)
    pass


@bot.message_handler(commands=['help'])  # выводим сообщение с целью указать, как правильно вводить функцию
def send_help(message):
    bot.send_message(message.from_user.id, "Важно ❗ Для конвертации волюты, необходимо вводить: \
        <имя валюты>пробел<в какую валюту переводим>пробел<количество>. \
                                                    Просмотреть доступную валюту можно: /values ⬅")
    pass


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = 'Доступная валюта:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)
    pass


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f'Слишком много параметров')

        quote, base, amount = values
        total_base = ConverterCurrency.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}📵')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
