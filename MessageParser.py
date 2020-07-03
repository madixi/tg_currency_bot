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
    _city_url_name = None
    _city_name = None
    _currency_code = None

    def parse(self, message):
        self._reset_values()
        message_text = message.text.lower()
        self._find_city(message_text)
        self._find_currency(message_text)

    def get_values(self):
        if self._currency_code is not None:
            if self._city_name is not None:
                return self._currency_code, \
                       self._city_url_name, \
                       self._city_name
            else:
                return ()
        else:
            return ()

    def _find_city(self, message: str):
        for i, city in enumerate(self.__CITIES_DATA['city_oblig_part']):
            if message.find(city) != -1:
                self._city_url_name = self.__CITIES_DATA.iloc[i][
                    "city_url_name"]
                self._city_name = self.__CITIES_DATA.iloc[i][
                    "city_name"]
                break

    def _find_currency(self, message: str):
        for i, currency_filter in enumerate(self.__CURRENCIES_DATA.keys()):
            if message.find(currency_filter) != -1:
                self._currency_code = self.__CURRENCIES_DATA[currency_filter]
                break

    def _reset_values(self):
        self._city_url_name = None
        self._city_name = None
        self._currency_code = None
