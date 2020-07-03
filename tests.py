import unittest

from CurrenciesPricesParser import CurrenciesPricesParser
from MessageParser import MessageParser


class MessageParserTest(unittest.TestCase):
    __message_parser = MessageParser()

    def test_city1(self):
        self.__message_parser._find_city(
            "Как же я люблю сидеть в Санкт-Петербурге и думать про доллары"
                .lower())
        self.assertEqual(self.__message_parser._city_url_name,
                         "sankt-peterburg",
                         'Should be "sankt-peterburg"')
        self.assertEqual(self.__message_parser._city_name,
                         "Санкт-Петербург", 'Should be "Санкт-Петербург"')
        self.__message_parser._reset_values()

    def test_city2(self):
        self.__message_parser._find_city(
            "А вот приеду в Краснодаре и буду покупать евро".lower())
        self.assertEqual(self.__message_parser._city_url_name, "krasnodar",
                         'Should be "krasnodar"')
        self.assertEqual(self.__message_parser._city_name,
                         "Краснодар", 'Should be "Краснодар"')
        self.__message_parser._reset_values()

    def test_city_no_city(self):
        self.__message_parser._find_city(
            "ывлпофж фл ывд фыда лфыждв л".lower())
        self.assertEqual(self.__message_parser._city_url_name, None,
                         'Should be None')
        self.assertEqual(self.__message_parser._city_name,
                         None, 'Should be None')
        self.__message_parser._reset_values()

    def test_currency1(self):
        self.__message_parser._find_currency(
            "А вот во Владивостоке куплю себе CNY".lower())
        self.assertEqual(self.__message_parser._currency_code, "cny",
                         'Should be "cny"')
        self.__message_parser._reset_values()

    def test_currency2(self):
        self.__message_parser._find_currency(
            "Приеду к брату в Томск - куплю себе йен".lower())
        self.assertEqual(self.__message_parser._currency_code, "jpy",
                         'Should be "jpy"')
        self.__message_parser._reset_values()

    def test_currency_no_currency(self):
        self.__message_parser._find_currency(
            "ывлпофж фл ывд фыда лфыждв л".lower())
        self.assertEqual(self.__message_parser._currency_code, None,
                         'Should be None')
        self.__message_parser._reset_values()


class CurrencyPricesParserTest(unittest.TestCase):
    __currency_prices_parser = CurrenciesPricesParser()

    def test_usd(self):
        self.assertEqual(self.__currency_prices_parser
                         .get_cb_price("usd", "20.03.2001".split(".")),
                         28.65, 'Should be 28.65')

    def test_eur(self):
        self.assertEqual(self.__currency_prices_parser
                         .get_cb_price("eur", "05.02.2000".split(".")),
                         28.49, 'Should be 28.49')

    def test_gbp(self):
        self.assertEqual(self.__currency_prices_parser
                         .get_cb_price("gbp", "23.06.2010".split(".")),
                         45.6427, 'Should be 45.6427')

    def test_cny(self):
        self.assertEqual(self.__currency_prices_parser
                         .get_cb_price("cny", "14.05.2019".split(".")),
                         95.2642, 'Should be 95.2642')

    def test_jpy(self):
        self.assertEqual(self.__currency_prices_parser
                         .get_cb_price("jpy", "03.07.2020".split(".")),
                         65.664, 'Should be 65.664')


if __name__ == '__main__':
    unittest.main()
