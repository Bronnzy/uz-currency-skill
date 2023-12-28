from mycroft import MycroftSkill, intent_file_handler, intent_handler
from .utils import CurrencyExchangeRate


class CurrencyRate(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler("ExchangeRate.intent")
    def handle_exchange_rate(self, message):
        currency = message.data.get("currency_a")
        message = CurrencyExchangeRate(currency_from=currency)
        message = message.get_currency_exchange_rate()

        if message["is_error"]:
            self.speak_dialog("Error", data={"error": message["data"]})
        else:
            self.speak_dialog(
                "CurrentRate",
                data={
                    "currency_name": message["currency_name"],
                    "rate": message["rate"],
                },
            )

    @intent_handler("CurrencyConversion.intent")
    def handle_currency_conversion(self, message):
        amount = message.data.get("amount")
        currency_from = message.data.get("currency_a")
        currency_to = message.data.get("currency_b")

        message = CurrencyExchangeRate(
            amount=amount, currency_from=currency_from, currency_to=currency_to
        )
        message = message.get_converted_currency()

        if message["is_error"]:
            self.speak_dialog("Error", data={"error": message["data"]})
        else:
            self.speak_dialog(
                "CurrencyConversion",
                data={
                    "amount": message["amount"],
                    "currency_from_name": message["currency_from_name"],
                    "currency_to_name": message["currency_to_name"],
                    "converted_amount": message["converted_amount"],
                },
            )


def create_skill():
    return CurrencyRate()
