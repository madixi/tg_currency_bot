import urllib.request
from time import sleep

import pandas as pd
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver


class CurrenciesPricesParser:
    __DEFAULT_URL = "https://www.banki.ru/products/currency/cash/<currency>/<city>/#bank-rates"
    __DEFAULT_CB_URL = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
    __driver_options = selenium.webdriver.FirefoxOptions()
    __driver_options.headless = True
    __driver = webdriver.Firefox(
        executable_path="./driver/geckodriver.exe",
        options=__driver_options)

    def __get_page(self, currency: str, city_url_name: str):
        url = self.__DEFAULT_URL \
            .replace("<currency>", currency) \
            .replace("<city>", city_url_name)
        self.__driver.get(url)
        sleep(3)
        soup = BeautifulSoup(self.__driver.page_source, features="html.parser")
        return soup

    def get_local_prices(self, currency: str,
                         city_url_name: str) -> pd.DataFrame:
        soup = self.__get_page(currency, city_url_name)
        with open("test.html", "w", encoding="utf-8") as out:
            out.writelines(str(soup))
        popup = soup.select('div[class="notice-popup"]')
        if len(popup) != 0:
            return None
        rows = soup.select('tr[data-test="bank-rates-row"]')
        bank_names = []
        selling_prices = []
        buying_prices = []
        for row in rows:
            bank_names.append(row.find('a').get_text())
            buying_prices.append(
                float(row.select('td[data-currencies-rate-buy]')[0]
                      ["data-currencies-rate-buy"]))
            selling_prices.append(
                float(row.select('td[data-currencies-rate-sell]')[0]
                      ["data-currencies-rate-sell"]))
        df = pd.DataFrame({"bank_name": bank_names,
                           "buying_price": buying_prices,
                           "selling_price": selling_prices
                           })
        if currency == "cny":
            df["selling_price"] = df["selling_price"].apply(
                lambda x: x * (1 + 9 * (x < 1.5))
            )
            df["buying_price"] = df["buying_price"].apply(
                lambda x: x * (1 + 9 * (x < 1.5))
            )
        df = df.groupby(by="bank_name") \
            .agg({"buying_price": 'max', "selling_price": "min"})
        df = df.reset_index()
        return df

    def get_cb_price(self, currency: str, date: tuple) -> float:
        url = self.__DEFAULT_CB_URL + date[0] + "/" + date[1] + "/" + date[2]
        with urllib.request.urlopen(url) as bytes:
            soup = BeautifulSoup(bytes.read(), features="html.parser")
        currency_data = soup.find("charcode", text=currency.upper()).parent
        price = float(currency_data.find("value").get_text().replace(",", "."))
        return price

    def run_tests(self):
        self.__get_cb_price_test()
        print("get_cb_price passed all tests")

    def __get_cb_price_test(self):
        assert self.get_cb_price("usd", "20.03.2001".split(".")) == 28.65
        assert self.get_cb_price("eur", "05.02.2000".split(".")) == 28.49
        assert self.get_cb_price("gbp", "23.06.2010".split(".")) == 45.6427
        assert self.get_cb_price("cny", "14.05.2019".split(".")) == 95.2642
        assert self.get_cb_price("jpy", "03.07.2020".split(".")) == 65.664
