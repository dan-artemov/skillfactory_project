import telebot
from config import TOKEN
from extensions import *

bot = telebot.TeleBot(TOKEN) # Создаем объект телеграм-бота

@bot.message_handler(commands=['start','help']) # обрабатываем команды start и help, отправляемые в чат-бот с выводом правил взаимодействия с ботом
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите через пробел команду боту в следующем формате: \n<имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты> ' \
           '\n Для вывода доступной валюты введите /values' \
           '\n Для вывода примеров ввода введите /examples'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values']) # обрабатываем команду values с выводом списка доступных валют
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in currency_code.keys():
        text = '\n    '.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=['examples']) # обрабатываем команду examples с выводом примеров вывода валюты
def values(message: telebot.types.Message):
    text = 'Примеры корректных сообщений телеграмм боту:' \
           '\n евро рубль 1' \
           '\n доллар рубль 100' \
           '\n евро доллар 1000'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',]) # обрабатываем введенных текст
def convert(message: telebot.types.Message): # основной модуль конвертации валют
    try:
        values = message.text.split(' ') # пытаемся записать кортеж в переменную

        if len(values) != 3: # если количество введенных параметров отличается от 3, срабатывает исключение
            raise ConvertException('Неверное количество параметров. \n Введите три параметра через пробел: \n<имя валюты> ' \
           '<в какую валюту перевести> ' \
           '<количество переводимой валюты>')
        base_code, target_code, amount = values # пытаемся распарсить кортеж по отдельным переменным
        cost = Сurrency_convertion.get_price(base_code, target_code, amount) # создаем объект класса, в рамках которого возвращается результат конвертации валюь
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}') # в случае ошибок конвертации выводим тип ошибки пользователю
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}') # в случае иных ошибок выводим содержимое ошибки
    else: # если ошибок не возникло готовим форматированный вывод текста и вывод сообщения в чат
        text = f'Цена {amount} {currency_code[base_code.lower()]} в {currency_code[target_code.lower()]} составляет: {cost} {currency_code[target_code.lower()]}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True, interval=0)
