import unittest
from unittest import TestCase
from unittest.mock import Mock, patch

from prestashop_orders_client.parser import _OrderParser
from prestashop_orders_client.utils import Order


class TestOrderParser(TestCase):

    def setUp(self):
        self.order_link = "https://example/api/orders/1"
        self.session = Mock()
        self.parser = _OrderParser(self.session)

    @patch.object(_OrderParser, "extract_order_data")
    @patch.object(_OrderParser, "parse_resource")
    def test_parse_order(self, mock_parse_resource, mock_extract_order_data):
        # Create mock return values for the extract_order_data and parse_resource method
        order_data = {
            "order": {'id': '200',
                      'total_paid': '90.000000',
                      'reference': 'ABCDEF'},
            "order_state": {'id': '4',
                            'name': {'language': {
                                '@id': '1', '@xlink:href': 'https://example/api/languages/1',
                                '#text': 'Shipped'}
                            }
                            },
            "customer": {'id': '999',
                         'email': 'example@example.co',
                         'id_gender': '1'},
            "address": {'id': '999',
                        'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'id_state': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'company': 'EA Sports', 'lastname': 'Doe', 'firstname': 'John',
                        'address1': '4530 Abra Kadabra', 'address2': 'And something else', 'postcode': '1234',
                        'city': 'Moscow', 'phone': '123456778', 'phone_mobile': '123456778'},
            "country": {'id_currency': '0', 'call_prefix': '971', 'iso_code': 'AE', 'active': '1',
                        'contains_states': '0', 'need_identification_number': '0', 'need_zip_code': '1',
                        'zip_code_format': None, 'display_tax_label': '1', 'name': {
                    'language': {'@id': '1', '@xlink:href': 'https://example/api/languages/1',
                                 '#text': 'United Arab Emirates'}}},
            "state": {'id': '44', 'id_zone': {'@xlink:href': 'https://example/api/zones/2', '#text': '2'},
                      'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                      'iso_code': 'SD', 'name': 'South Dakota', 'active': '1'}
        }
        mock_extract_order_data.return_value = order_data

        # Create a mock return value for the parse_resource method
        mock_parse_resource.side_effect = [
            {'id': 200, 'total_paid': 90.0, 'reference': 'ABCDEF'},
            {'order_state': 'Shipped'},
            {'email': 'example@example.co'},
            {'first_name': 'John', 'last_name': 'Doe', 'company_name': 'EA Sports',
             'phone': '123456778', 'address': '4530 Abra Kadabra And something else',
             'city': 'Moscow', 'post_code': '1234'},
            {'country': 'United Arab Emirates'},
            {'state': 'South Dakota'}
        ]

        # Call the method under test
        result = self.parser.parse_order(self.order_link)

        # Assert that the result is what we expect
        expected_result = Order(id=200, total_paid=90.000000, reference='ABCDEF',
                                order_state="Shipped",
                                email="example@example.co",
                                first_name="John", last_name="Doe", company_name="EA Sports", phone="123456778",
                                address="4530 Abra Kadabra And something else", city="Moscow", post_code="1234",
                                country="United Arab Emirates",
                                state="South Dakota",
                                )
        self.assertIsInstance(result, Order)
        self.assertEqual(result, expected_result)

        # Assert that extract_order_data and parse_resource method were called with expected args
        mock_extract_order_data.assert_called_once_with(self.order_link)
        mock_parse_resource.assert_has_calls([
            unittest.mock.call("order", order_data["order"]),
            unittest.mock.call("order_state", order_data["order_state"]),
            unittest.mock.call("customer", order_data["customer"]),
            unittest.mock.call("address", order_data["address"]),
            unittest.mock.call("country", order_data["country"]),
            unittest.mock.call("state", order_data["state"]),
        ])

    @patch("prestashop_orders_client.parser._get_resource_as_dict")
    def test_extract_order_data_with_state(self, mock__get_resource_as_dict: Mock):
        order_data = {"id": "999",
                      'current_state': {'@xlink:href': 'https://example/api/order_states/4', '#text': '4'},
                      'id_address_delivery': {'@xlink:href': 'https://example/api/addresses/1', '#text': '1'},
                      'id_customer': {'@xlink:href': 'https://example/api/customers/1', '#text': '1'},
                      }
        order_state_data = {"order_state_data": "order_state_data"}
        customer_data = {"customer_data": "customer_data"}
        address_data = {"id": "999",
                        'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'id_state': {'@xlink:href': 'https://example/api/states/44', '#text': '44'}}
        country_data = {"country_data": "country_data"}
        state_data = {"state_data": "state_data"}

        mock__get_resource_as_dict.side_effect = [order_data, order_state_data,
                                                  customer_data, address_data,
                                                  country_data, state_data]
        expected_result = {
            "order": order_data,
            "order_state": order_state_data,
            "customer": customer_data,
            "address": address_data,
            "country": country_data,
            "state": state_data
        }
        result = self.parser.extract_order_data(self.order_link)

        self.assertDictEqual(result, expected_result)

    @patch("prestashop_orders_client.parser._get_resource_as_dict")
    def test_extract_order_data_without_state(self, mock__get_resource_as_dict: Mock):
        order_data = {"id": "999",
                      'current_state': {'@xlink:href': 'https://example/api/order_states/4', '#text': '4'},
                      'id_address_delivery': {'@xlink:href': 'https://example/api/addresses/1', '#text': '1'},
                      'id_customer': {'@xlink:href': 'https://example/api/customers/1', '#text': '1'},
                      }
        order_state_data = {"order_state_data": "order_state_data"}
        customer_data = {"customer_data": "customer_data"}
        address_data = {"id": "999",
                        'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'id_state': '0'}
        country_data = {"country_data": "country_data"}

        mock__get_resource_as_dict.side_effect = [order_data, order_state_data,
                                                  customer_data, address_data,
                                                  country_data]
        expected_result = {
            "order": order_data,
            "order_state": order_state_data,
            "customer": customer_data,
            "address": address_data,
            "country": country_data,
            "state": {}
        }
        result = self.parser.extract_order_data(self.order_link)

        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_order(self):
        order_data = {'id': '200',
                      'total_paid': '90.000000',
                      'reference': 'ABCDEF'}
        result = self.parser.parse_resource("order", order_data)
        expected_result = {'id': 200, 'total_paid': 90.0, 'reference': 'ABCDEF'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_order_state(self):
        order_state_data = {'id': '4',
                            'name': {'language': {
                                '@id': '1', '@xlink:href': 'https://example/api/languages/1',
                                '#text': 'Shipped'}
                            }
                            }
        result = self.parser.parse_resource("order_state", order_state_data)
        expected_result = {'order_state': 'Shipped'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_customer(self):
        customer_data = {'id': '999',
                         'email': 'example@example.co',
                         'id_gender': '1'}
        result = self.parser.parse_resource("customer", customer_data)
        expected_result = {'email': 'example@example.co'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_address_with_all_fields(self):
        address_data = {'id': '999',
                        'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'id_state': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'company': 'EA Sports', 'lastname': 'Doe', 'firstname': 'John',
                        'address1': '4530 Abra Kadabra', 'address2': 'And something else', 'postcode': '1234',
                        'city': 'Moscow', 'phone': '123456778', 'phone_mobile': '123456778'}
        result = self.parser.parse_resource("address", address_data)
        expected_result = {'first_name': 'John', 'last_name': 'Doe', 'company_name': 'EA Sports',
                           'phone': '123456778', 'address': '4530 Abra Kadabra And something else',
                           'city': 'Moscow', 'post_code': '1234'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_address_with_mandatory_fields(self):
        address_data = {'id': '999',
                        'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'id_state': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                        'company': None, 'lastname': 'Doe', 'firstname': 'John',
                        'address1': '4530 Abra Kadabra', 'address2': None, 'postcode': '1234',
                        'city': 'Moscow', 'phone': '123456778', 'phone_mobile': '123456778'}
        result = self.parser.parse_resource("address", address_data)
        expected_result = {'first_name': 'John', 'last_name': 'Doe', 'company_name': None,
                           'phone': '123456778', 'address': '4530 Abra Kadabra',
                           'city': 'Moscow', 'post_code': '1234'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_country(self):
        country_data = {'id_currency': '0', 'call_prefix': '971', 'iso_code': 'AE', 'active': '1',
                        'contains_states': '0', 'need_identification_number': '0', 'need_zip_code': '1',
                        'zip_code_format': None, 'display_tax_label': '1', 'name': {
                'language': {'@id': '1', '@xlink:href': 'https://example/api/languages/1',
                             '#text': 'United Arab Emirates'}}}
        result = self.parser.parse_resource("country", country_data)
        expected_result = {'country': 'United Arab Emirates'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_not_none_state(self):
        state_data = {'id': '44', 'id_zone': {'@xlink:href': 'https://example/api/zones/2', '#text': '2'},
                      'id_country': {'@xlink:href': 'https://example/api/countries/21', '#text': '21'},
                      'iso_code': 'SD', 'name': 'South Dakota', 'active': '1'}
        result = self.parser.parse_resource("state", state_data)
        expected_result = {'state': 'South Dakota'}
        self.assertDictEqual(result, expected_result)

    def test_parse_resource_on_none_state(self):
        state_data = {}
        result = self.parser.parse_resource("state", state_data)
        expected_result = {'state': None}
        self.assertDictEqual(result, expected_result)
