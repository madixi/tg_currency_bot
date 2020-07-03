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

    def run_tests(self):
        self.__message_parse_tests()

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

    def __message_parse_tests(self):
        self.__find_city(
            "Как же я люблю сидеть в Санкт-Петербурге и думать про доллары"
                .lower())
        assert self.__city_url_name == "sankt-peterburg"
        assert self.__city_name == "Санкт-Петербург"
        self.__reset_values()

        self.__find_city(
            "А вот приеду в Краснодаре и буду покупать евро".lower())
        assert self.__city_url_name == "krasnodar"
        assert self.__city_name == "Краснодар"
        self.__reset_values()

        self.__find_city(
            "ывлпофж фл ывд фыда лфыждв л".lower())
        assert self.__city_url_name is None
        assert self.__city_name is None
        self.__reset_values()

        self.__find_currency(
            "А вот во Владивостоке куплю себе CNY".lower())
        assert self.__currency_code == "cny"
        self.__reset_values()

        self.__find_currency(
            "Приеду к брату в Томск - куплю себе йен".lower())
        assert self.__currency_code == "jpy"
        self.__reset_values()

        self.__find_currency(
            "ывлпофж фл ывд фыда лфыждв л")
        assert self.__currency_code is None
        self.__reset_values()

        print("MessageParser passed all tests")
