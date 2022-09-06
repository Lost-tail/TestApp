import requests
from datetime import date
import xml.etree.ElementTree as ET


class Converter:
    
    URL = 'http://www.cbr.ru/scripts/XML_dynamic.asp'
    USD = 'R01235'

    @classmethod
    def get_currency_rate(cls, currency: str) -> float:
        today = date.today().strftime('%d/%m/%Y')
        response = requests.get(cls.URL + f"?date_req1={today}&date_req2={today}&VAL_NM_RQ={getattr(cls, currency.upper())}").text
        return float(ET.fromstring(response)[0][1].text.replace(',', '.'))

    @classmethod
    def usd_to_rub(cls, amount: float) -> float:
        return round(amount*cls.get_currency_rate('usd'), 2)
