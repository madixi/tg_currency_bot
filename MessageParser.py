import pandas as pd


class MessageParser:
    __CURRENCIES_DATA = {
        "usd": "usd",
        "доллар": "usd",
        "бакс": "usd",
        "eur": "eur",
        "евро": "eur",
        "gbp": "gbp",
        "фунт": "gbp",
        "jpy": "jpy",
        "йен": "jpy",
        "иен": "jpy",
        "cny": "cny",
        "юан": "cny",
    }
    __CITIES_DATA = pd.read_csv("cities_data.csv")
    __city_url_name = None
    __city_name = None
    __currency_code = None

    def parse(self, message):
        self.__reset_values()
        message_text = message.text.lower()
        self.__find_city(message_text)
        self.__find_currency(message_text)

    def get_values(self):
        if self.__currency_code is not None:
            if self.__city_name is not None:
                return self.__currency_code, \
                       self.__city_url_name, \
                       self.__city_name
            else:
                return ()
        else:
            return ()

    def __find_city(self, message: str):
        for i, city in enumerate(self.__CITIES_DATA['city_oblig_part']):
            if message.find(city) != -1:
                self.__city_url_name = self.__CITIES_DATA.iloc[i][
                    "city_url_name"]
                self.__city_name = self.__CITIES_DATA.iloc[i][
                    "city_name"]
                break

    def __find_currency(self, message: str):
        for i, currency_filter in enumerate(self.__CURRENCIES_DATA.keys()):
            if message.find(currency_filter) != -1:
                self.__currency_code = self.__CURRENCIES_DATA[currency_filter]
                break

    def __reset_values(self):
        self.__city_url_name = None
        self.__city_name = None
        self.__currency_code = None
