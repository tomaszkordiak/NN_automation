import json

from clients.baseClient import BaseClient
from config import BASE_URL, ENDPOINT
from utils.data_generator import Data
from utils.request import APIRequest


class PaymentClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.base_url = BASE_URL
        self.endpoint = ENDPOINT
        self.request = APIRequest()

    def create_payment(self, user=None, purchase=None, amount=None, currency=None):
        user = user if user else Data.user
        password = user

        purchase = purchase if purchase else Data.purchase
        amount = amount if amount else Data.amount
        currency = currency if currency else Data.currency

        # create json
        payload = json.dumps({
            'purchase': purchase,
            'amount': amount,
            'currency': currency
        })

        response = self.request.put(url=self.base_url + self.endpoint,
                                    payload=payload,
                                    headers=self.headers,
                                    auth=(user, password))

        return response

    def process_payments(self):
        user = Data.user
        password = user

        response = self.request.post(BASE_URL + ENDPOINT, headers=self.headers, auth=("admin", "admin"))
        return response

    def get_all_payments(self):
        user = Data.user
        password = user

        response = self.request.get(BASE_URL + ENDPOINT, auth=(user, password))
        return response

    def delete_payment(self, payment_id):
        user = Data.user
        password = user

        response = self.request.delete(BASE_URL + ENDPOINT + f"/{payment_id}", auth=(user, password))
        return response
