import requests
from thefuzz import process

EXCHANGE_RATE_API_URL = "https://cbu.uz/oz/arkhiv-kursov-valyut/json/"


class CurrencyExchangeRate:
    def __init__(self, currency_from=None, currency_to=None, amount=None):
        self.message = dict()
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.amount = amount
        self.data = self._load_data()

    def _load_data(self):
        response = requests.get(EXCHANGE_RATE_API_URL)
        return response.json()

    def _extract_currency(self, currency):
        """
        Extracts the best fit currency that match currency_from attribute

        Returns: currency object
        """
        collection = [item["CcyNm_UZ"] for item in self.data]
        result = process.extract(currency, collection)[0][0]
        matched_currency = next(
            (
                currency_obj
                for currency_obj in self.data
                if currency_obj["CcyNm_UZ"] == result
            ),
            None,
        )
        return matched_currency

    def get_currency_exchange_rate(self):
        """
        Returns exchange rate for specific currency
        """
        currency = self._extract_currency(self.currency_from)
        if not currency:
            self.message.update(
                data="Kechirasiz, valyuta nomini tushunaolmadim", is_error=True
            )
            return self.message

        self.message.update(
            rate=currency["Rate"], currency_name=currency["CcyNm_UZ"], is_error=False
        )
        return self.message

    def get_converted_currency(self):
        currency_from = self._extract_currency(self.currency_from)
        currency_to = self._extract_currency(self.currency_to)
        try:
            currency_from_rate = float(currency_from["Rate"])
            currency_to_rate = float(currency_to["Rate"])
            amount = float(self.amount)
        except ValueError:
            self.message.updata(
                data="Qiymatni tushunaolmadim, aniqroq aytishga harakat qiling!",
                is_error=True,
            )
            return self.message

        converted_amount = round((currency_from_rate / currency_to_rate) * amount, 2)
        self.message.update(
            currency_from_name=currency_from["CcyNm_UZ"],
            currency_to_name=currency_to["CcyNm_UZ"],
            amount=self.amount,
            converted_amount=converted_amount,
            is_error=False,
        )
        return self.message


if __name__ == "__main__":
    message = CurrencyExchangeRate(
        currency_from="dollar", currency_to="Angliya funt sterlingi", amount=20
    )
    message = message.get_converted_currency()
    print(message)
