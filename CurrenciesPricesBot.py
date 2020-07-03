import re

import telebot

from CurrenciesPricesParser import CurrenciesPricesParser
from MessageParser import MessageParser

MAX_BANK_NAME_LEN = 20
MAX_PRICE_LEN = 6
START_LINE_PATTERN = "```\n╔" + "═" * MAX_BANK_NAME_LEN + "╤" + "═" * 6 + "╗\n"
END_LINE_PATTERN = "╚" + "═" * MAX_BANK_NAME_LEN + "╧" + "═" * MAX_PRICE_LEN \
                   + "╝\n```"
START_MESSAGE = "🤖 Бот автоматически разбирает сообщения и отвечает, если появлялась валюта и город.\n"\
                "☑ Разрешенные валюты 💸: USD, EUR, GBP, CNY, JPY (код или слово)\n"\
                "🇷🇺 На данный момент поддерживаются административные центры всех 85 регинов\n"\
                "☑ Также можно узнать курс ЦБ РФ по валюте в опрделенный день (/cb)"


def get_table_row(bank_name: str, price: float):
    price = str(price)
    output = "║"
    output += bank_name
    output += (MAX_BANK_NAME_LEN - len(bank_name)) * " "
    output += "|"
    output += price
    output += (MAX_PRICE_LEN - len(price) - 1) * " "
    output += "р║\n"
    return output


with open("API_Token", "r") as inp:
    API_Token = inp.readline()
bot = telebot.TeleBot(API_Token)
currency_parser = CurrenciesPricesParser()
message_parser = MessageParser()


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Бот с курсами валют 💵💶💷💴")
    bot.send_message(message.chat.id, START_MESSAGE)


@bot.message_handler(commands=['cb'])
def handle_cb(message):
    if re.match(r"^/cb [A-Za-z]{3} [0-9]{2}[./][0-9]{2}[./][0-9]{4}$",
                message.text) is None:
        bot.send_message(message.chat.id, "Использование команды:\n"
                                          "/cb <код валюты> <дата> \n"
                                          "Примеры:\n"
                                          "☑ /cb usd 20.09.2005\n"
                                          "☑ /cb JPY 20/09/2005")
    else:
        _, currency_code, date = message.text.split()
        date = date.replace("/", ".")
        price = currency_parser.get_cb_price(currency_code, date.split("."))
        output = f"💹Курс {currency_code.upper()} " \
                 f"на {date} согласно ЦБ РФ: {price}р"
        bot.reply_to(message, output)


@bot.message_handler()
def handle_any_message(message):
    message_parser.parse(message)
    parsed_data = message_parser.get_values()
    if len(parsed_data) == 3:
        bot_message = bot.reply_to(message, "Обрабатываю ⌛ ")
        currency = parsed_data[0]
        city_url = parsed_data[1]
        city = parsed_data[2]
        currency_rates = currency_parser \
            .get_local_prices(currency, city_url)
        if currency_rates is None:
            bot.edit_message_text(
                f"Данных по {currency.upper()}в г. {city} нет",
                chat_id=message.chat.id,
                message_id=bot_message.message_id)
        else:
            output = f"🔄 Лучшие курсы {currency.upper()} в г. {city}: \n "
            output += "Купить:\n"
            best_offers = currency_rates \
                              .sort_values(by="selling_price") \
                              .reset_index().iloc[:5]
            for i in range(best_offers.shape[0]):
                bank_name = best_offers.iloc[i]['bank_name']
                price = best_offers.loc[i, 'selling_price']
                output += "💵 " + str(price)
                output += (MAX_PRICE_LEN - len(str(price))) * "0"
                output += "р 🏦 " + bank_name + "\n"

            output += f"\nПродать: \n"
            best_offers = currency_rates \
                              .sort_values(by="buying_price", ascending=False) \
                              .reset_index() \
                              .iloc[:5]
            for i in range(best_offers.shape[0]):
                bank_name = best_offers.iloc[i]['bank_name']
                price = best_offers.loc[i, 'buying_price']
                output += "💵 " + str(price)
                output += (MAX_PRICE_LEN - len(str(price))) * "0"
                output += "р 🏦 " + bank_name + "\n"
            bot.edit_message_text(output,
                                  chat_id=message.chat.id,
                                  message_id=bot_message.message_id,
                                  parse_mode="Markdown")


bot.polling()
