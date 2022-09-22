import json
from utils.data_generator import Data
from clients.paymentClient import PaymentClient
import requests
from config import BASE_URL, USERS, ENDPOINT, HEADERS
from assertpy.assertpy import assert_that

client = PaymentClient()


def setup_method():
    print("before test")


def test_welcome_text_guest_user():
    response = requests.get(BASE_URL)

    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.text).is_equal_to("Welcome, Guest!")


def test_welcome_text_logged_user():
    for user in USERS:
        response = requests.get(BASE_URL, auth=(user, user))

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.text).is_equal_to(f"Welcome, {user}!")


def test_delete_all_payments():
    data = client.get_all_payments().as_dict
    payments = data['payments']
    ids = [payment[0] for payment in payments]
    for _id in ids:
        response = client.delete_payment(payment_id=_id)
        assert_that(response.status_code).is_equal_to(200)
        assert_that((response.as_dict['deleted'])).is_equal_to(1)
    payments_empty = client.get_all_payments().as_dict['payments']
    assert_that(payments_empty).is_empty()


def test_delete_single_payment():
    # create payment and check status code
    user = Data.user
    purchase = Data.purchase
    amount = Data.amount
    currency = Data.currency

    response = client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
    assert_that(response.status_code).is_equal_to(200)

    # get all payments and filter over the one created before
    data = client.get_all_payments().as_dict
    payments = data['payments']

    payment_created = filter(lambda payment: payment[1] == purchase and payment[2] == user
                                             and payment[3] == amount
                                             and payment[4] == currency
                                             and payment[5] == 0, payments)

    # get id of the payment and delete it
    id_payment_created = list(payment_created)[0][0]
    response = client.delete_payment(id_payment_created)
    assert_that(response.status_code).is_equal_to(200)
    assert_that((response.as_dict['deleted'])).is_equal_to(1)


def test_new_payment_can_be_added():
    # create payment and check status code
    user = Data.user
    purchase = Data.purchase
    amount = Data.amount
    currency = Data.currency

    response = client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
    assert_that(response.status_code).is_equal_to(200)

    # get list of all payments and filter over the one that was sent
    data = client.get_all_payments().as_dict
    payments = data['payments']

    payment_created = filter(lambda payment: payment[1] == purchase and payment[2] == user
                                             and payment[3] == amount
                                             and payment[4] == currency
                                             and payment[5] == 0, payments)
    payment_created = list(payment_created)[0]
    assert_that(payment_created).is_not_empty()
    assert_that(payment_created[0]).is_type_of(int)


def test_many_payments_can_be_added():
    for i in range(100):
        # create payment and check status code
        user = Data.user
        purchase = Data.purchase
        amount = Data.amount
        currency = Data.currency

        response = client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
        assert_that(response.status_code).is_equal_to(200)

        # get list of all payments and filter over the one that was sent
        data = client.get_all_payments().as_dict
        payments = data['payments']

        payment_created = filter(lambda payment: payment[1] == purchase and payment[2] == user
                                                 and payment[3] == amount
                                                 and payment[4] == currency
                                                 and payment[5] == 0, payments)
        payment_created = list(payment_created)[0]
        assert_that(payment_created).is_not_empty()
        assert_that(payment_created[0]).is_type_of(int)
