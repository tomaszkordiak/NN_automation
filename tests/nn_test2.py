from utils.data_generator import Data
from clients.paymentClient import PaymentClient
import requests
from config import BASE_URL, USERS
from assertpy.assertpy import assert_that


class TestClass:
    client = PaymentClient()

    def setup_method(self, test_method):
        self._delete_all_payments()

    def teardown_method(self, test_method):
        self._delete_all_payments()

    def test_welcome_text_guest_user(self):
        response = requests.get(BASE_URL)

        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.text).is_equal_to("Welcome, Guest!")

    def test_welcome_text_logged_user(self):
        for user in USERS:
            response = requests.get(BASE_URL, auth=(user, user))

            assert_that(response.status_code).is_equal_to(200)
            assert_that(response.text).is_equal_to(f"Welcome, {user}!")

    def test_delete_single_payment(self):
        # create payment and check status code
        user = Data.user
        purchase = Data.purchase
        amount = Data.amount
        currency = Data.currency

        response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
        assert_that(response.status_code).is_equal_to(200)

        # get all payments and filter over the one created before
        data = self.client.get_all_payments().as_dict
        payments = data['payments']

        payment_created = filter(lambda payment: payment[1] == purchase and payment[2] == user
                                                 and payment[3] == amount
                                                 and payment[4] == currency
                                                 and payment[5] == 0, payments)

        # get id of the payment and delete it
        id_payment_created = list(payment_created)[0][0]
        response = self.client.delete_payment(id_payment_created)
        assert_that(response.status_code).is_equal_to(200)
        assert_that((response.as_dict['deleted'])).is_equal_to(1)

    def test_delete_non_existing_payment(self):

        # get all payments and verify table is empty
        data = self.client.get_all_payments().as_dict['payments']
        assert_that(data).is_empty()

        # delete non-existing payment
        id_payment = 1
        response = self.client.delete_payment(id_payment)
        assert_that(response.status_code).is_equal_to(200)
        assert_that((response.as_dict['deleted'])).is_equal_to(0)

    def test_new_payment_can_be_added(self):
        # create payment and check status code
        user = Data.user
        purchase = Data.purchase
        amount = Data.amount
        currency = Data.currency

        response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
        assert_that(response.status_code).is_equal_to(200)

        # get list of all payments and filter over the one that was sent
        data = self.client.get_all_payments().as_dict
        payments = data['payments']

        payment_created = filter(lambda payment: payment[1] == purchase and payment[2] == user
                                                 and payment[3] == amount
                                                 and payment[4] == currency
                                                 and payment[5] == 0, payments)
        payment_created = list(payment_created)[0]
        assert_that(payment_created).is_not_empty()
        assert_that(payment_created[0]).is_type_of(int)

    def test_many_payments_can_be_added(self):
        for i in range(100):
            # create payment and check status code
            user = Data.user
            purchase = Data.purchase
            amount = Data.amount
            currency = Data.currency

            response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
            assert_that(response.status_code).is_equal_to(200)

            # get list of all payments and filter over the one that was sent
            data = self.client.get_all_payments().as_dict
            payments = data['payments']

            payment_created = filter(lambda payment: payment[1] == purchase and payment[2] == user
                                                     and payment[3] == amount
                                                     and payment[4] == currency
                                                     and payment[5] == 0, payments)
            payment_created = list(payment_created)[0]
            assert_that(payment_created).is_not_empty()
            assert_that(payment_created[0]).is_type_of(int)

    # This one should fail
    def test_create_payment_invalid_values(self):
        # create payment and check status code
        user = Data.user
        purchase = -1
        amount = -2456.65
        currency = "z3423232"

        response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
        assert_that(response.status_code).is_not_equal_to(200)  # should be more precise

    def test_process_single_payment(self):
        # create payment and check status code
        user = Data.user
        purchase = Data.purchase
        amount = Data.amount
        currency = Data.currency

        response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.as_dict['created']).is_equal_to(1)

        # check attributes of a new payment
        payment = self.client.get_all_payments().as_dict['payments'][0]
        assert_that(payment[-1]).is_equal_to(0)

        # process payment
        response = self.client.process_payments()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.as_dict['processed']).is_equal_to(1)
        print(response.as_dict)

        # check attributes of processed payment
        payment = self.client.get_all_payments().as_dict['payments'][0]
        assert_that(payment[-1]).is_equal_to(1)
        assert_that(payment[-2]).is_equal_to("EUR")

    def test_process_many_payments(self):
        # create many payments and check status code
        for i in range(100):
            user = Data.user
            purchase = Data.purchase
            amount = Data.amount
            currency = Data.currency

            response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
            assert_that(response.status_code).is_equal_to(200)

        # Get all payments and check that "Processed" is set to 0
        payments = self.client.get_all_payments().as_dict['payments']
        for payment in payments:
            assert_that(payment[-1]).is_equal_to(0)

        # process payments
        response = self.client.process_payments()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.as_dict['processed']).is_equal_to(100)

        # Get all payments and check that "Processed" is set to 1 and "Currency" to "EUR"
        payments = self.client.get_all_payments().as_dict['payments']
        for payment in payments:
            assert_that(payment[-1]).is_equal_to(1)
            assert_that(payment[-2]).is_equal_to("EUR")

        # create another 100 payments
        for i in range(100):
            user = Data.user
            purchase = Data.purchase
            amount = Data.amount
            currency = Data.currency

            response = self.client.create_payment(user=user, purchase=purchase, amount=amount, currency=currency)
            assert_that(response.status_code).is_equal_to(200)

        # Get all payments and check that for the last 100 "Processed" is set to 0
        payments = self.client.get_all_payments().as_dict['payments']
        for payment in payments[100:]:
            assert_that(payment[-1]).is_equal_to(0)

        # process rest of the payments
        response = self.client.process_payments()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.as_dict['processed']).is_equal_to(100)

        # Get all payments and check that "Processed" is set to 1 and "Currency" to "EUR"
        payments = self.client.get_all_payments().as_dict['payments']
        for payment in payments:
            assert_that(payment[-1]).is_equal_to(1)
            assert_that(payment[-2]).is_equal_to("EUR")

    def _delete_all_payments(self):
        data = self.client.get_all_payments().as_dict
        payments = data['payments']
        ids = [payment[0] for payment in payments]
        for _id in ids:
            response = self.client.delete_payment(payment_id=_id)
            assert_that(response.status_code).is_equal_to(200)
            assert_that((response.as_dict['deleted'])).is_equal_to(1)
        payments_empty = self.client.get_all_payments().as_dict['payments']
        assert_that(payments_empty).is_empty()
