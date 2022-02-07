import requests  # Module for URL processing
from bs4 import BeautifulSoup  # Module for working with html


class CurrencyConverter:
    LINK_TEMPLATE = 'https://www.google.com/search?q=$FROM+to+$TO+exchange+rate'  # Template of link to the desired page
    HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'}

    @staticmethod
    def get_currency_exchange_rate(source_currency: str, final_currency: str) -> float:
        """
        :param source_currency: Name of the currency to be converted from
        :param final_currency: Name of the currency to be converted to
        :return: the cost of source_currency in final_currency
        """

        # Generate a link to a request with the specified currencies
        link = CurrencyConverter.LINK_TEMPLATE.replace("$FROM", source_currency).replace("$TO", final_currency)

        full_page = requests.get(link, headers=CurrencyConverter.HEADERS)  # Get all html of page
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "DFlfde SwHCTb", "data-precision": 2})  # Get span with exchange_rate
        exchange_rate_str = convert[0].text  # Exchange_rate in string format (example: "100,00")
        return float(exchange_rate_str.replace(",", "."))


def mainloop():
    print(CurrencyConverter.get_currency_exchange_rate("dollar", "rub"))


if __name__ == "__main__":
    mainloop()
