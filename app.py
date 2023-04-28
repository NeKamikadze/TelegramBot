import telebot
from config import TOKEN, keys
from extensions import APIException, CashConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    name = message.from_user.first_name
    text = f'Приветствую, {name}!\nЯ чат-бот, который поможет узнать текущий курс обмена валют.\nЧтобы начать работу, ' \
           f'введите команду в следующем формате:\n<наименование валюты, стоимость которой хотите узнать> ' \
           f'<наименование валюты, в которую необходимо перевести> <количество переводимой валюты>\n' \
           'Чтобы увидеть список всех доступных валют, введите команду: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_(message: telebot.types.Message):
    text = 'Список доступных валют: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Указано неверное количество параметров!')

        base, quote, amount = values
        result = CashConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'{amount} "{keys[base.lower()]}" = {result} "{keys[quote.lower()]}"'
        bot.send_message(message.chat.id, text)


bot.polling()
