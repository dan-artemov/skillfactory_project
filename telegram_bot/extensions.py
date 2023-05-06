import requests
import json
from config import currency_code, API_Key

class ConvertException(Exception): # создаем класс, наследуемый от класса Exception
    pass

class Сurrency_convertion: # создаем класс конвертации валют содержащий основной обработчик ошибок
    @staticmethod
    def get_price(base_code: str, target_code: str, amount: str): # внути класса создаем статический метод осуществляющий запрос цены через внешний API
        if base_code == target_code: # проверяем не введены ли одинаковые валюты
            raise ConvertException(f' Вы пытаетесь конвертировать одинаковые валюты - "{base_code}"')
        try:# пытаемся присвоить значение ключа переменной, если ключ отсутсвует (т.е. пользвателем валюта введена неверно, то вызов ошибки)
            base = currency_code[base_code.lower()]
        except KeyError:
            raise ConvertException(f'Не удалось найти валюту "{base_code}". \n Список доступных валют по команде /values')
        try: # пытаемся присвоить значение ключа переменной, если ключ отсутсвует (т.е. пользвателем валюта введена неверно, то вызов ошибки)
            quote = currency_code[target_code.lower()]
        except KeyError:
            raise ConvertException(f'Не удалось найти валюту "{target_code}".  \n Список доступных валют по команде /values')
        try: # пытаемся преобразовать количество валюты к числу с плавающей запятой, в случае ошибки генерация сообщения
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertException(
                f'Не удалось обработать количество валюты "{amount}". \n Убедитесь, что введены числовые значения.')
        # с помощью get-запроса библиотеки requests по обращаемся к URL предоставляющему API для конвертации валюты
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API_Key}/pair/{base}/{quote}')
        # преобразовавываем с помощью json результат запроса в словарь и обращаемся к элементу словаря,
        # содержащему результат конвертации для единицы валюты, после чего умножаем на количество конвертируемой валюты
        cost = float(json.loads(r.content)['conversion_rate']) * amount
        return cost