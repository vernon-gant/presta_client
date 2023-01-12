from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from prestashop_orders_client.client import PrestaShopOrderClient
from prestashop_orders_client.exceptions import OrdersNotFound, PrestaShopConnectionError, \
    UnexpectedStatusCodeError, \
    WebServiceUnavailableError, InvalidApiKeyError, InvalidOrderNumber
from prestashop_orders_client.utils import Order
from prestashop_orders_client.parser import _OrderParser


class TestPrestaShopOrderClient(TestCase):

    def setUp(self):
        self.shop_link = "test_shop_link"
        self.api_key = "test_api_key"

    @patch.object(_OrderParser, "parse_order")
    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__establish_connection')
    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__count_orders')
    def test_get_valid_order(self, mock_count_orders, mock_establish_connection: Mock, mock_parse_order: Mock):
        # Set up the mock __establish_connection method to return the mock session
        mock_establish_connection.return_value = Mock()
        # Set up the mock to return a dictionary with two orders
        mock_count_orders.return_value = 10
        # Set up the mock to return a valid order
        mock_parse_order.return_value = Mock(spec=Order)
        # Initialize the PrestaShopApi object
        api = PrestaShopOrderClient(self.shop_link, self.api_key)
        # Call the get_order method
        order = api.get_order(5)

        self.assertIsInstance(order, Order)
        # Check that the mock __establish_connection method was called
        mock_count_orders.assert_called_once()
        # Check that the mock __count_orders method was called
        mock_establish_connection.assert_called_once_with(self.api_key)
        # Check that the mock parse_order method was called
        mock_parse_order.assert_called_once_with(f"https://{self.shop_link}/api/orders/5")

    @patch.object(_OrderParser, "parse_order")
    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__establish_connection')
    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__count_orders')
    def test_get_invalid_order(self, mock_count_orders, mock_establish_connection: Mock, mock_parse_order: Mock):
        # Set up the mock __establish_connection method to return the mock session
        mock_establish_connection.return_value = Mock()
        # Set up the mock to return a dictionary with two orders
        mock_count_orders.return_value = 10
        # Set up the mock to return a valid order
        mock_parse_order.return_value = Mock(spec=Order)
        # Initialize the PrestaShopApi object
        api = PrestaShopOrderClient(self.shop_link, self.api_key)
        # Call the get_order method
        with self.assertRaises(InvalidOrderNumber):
            api.get_order(11)

    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__establish_connection')
    @patch("prestashop_orders_client.client._get_resource_as_dict")
    def test_count_orders(self, mock__get_resource_as_dict: Mock, mock_establish_connection: Mock):
        # Set up the mock __establish_connection method to return the mock session
        mock_establish_connection.return_value = Mock()

        # Set up the mock to return a dictionary with two orders
        mock__get_resource_as_dict.return_value = {"order": [{}, {}]}

        # Initialize the PrestaShopApi object
        api = PrestaShopOrderClient(self.shop_link, self.api_key)

        # Check that the orders_amount attribute is set to 2
        self.assertEqual(api.orders_amount, 2)

    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__establish_connection')
    @patch("prestashop_orders_client.client._get_resource_as_dict")
    def test_count_orders_with_zero_orders(self, mock__get_resource_as_dict: Mock, mock_establish_connection: Mock):
        # Set up the mock __establish_connection method to return the mock session
        mock_establish_connection.return_value = Mock()
        # Set up the mock to return an empty dictionary
        mock__get_resource_as_dict.return_value = {}
        # Assert that the OrdersNotFound exception is raised
        with self.assertRaises(OrdersNotFound):
            PrestaShopOrderClient(self.shop_link, self.api_key)

    @patch.object(PrestaShopOrderClient, '_PrestaShopOrderClient__count_orders')
    @patch('requests.Session.get')
    def test_establish_connection_success(self, mock_session_get: Mock, mock_count_orders: Mock):
        # Set up the mock session to return a 200 status code
        mock_response = Mock()
        mock_response.status_code = 200
        mock_session_get.return_value = mock_response
        # Set up the mock count_orders method to return 1
        mock_count_orders.return_value = 1
        # Initialize the PrestaShopApi object
        api = PrestaShopOrderClient(self.shop_link, self.api_key)
        # Check that the __session attribute is set to the mock session
        self.assertIsInstance(api, PrestaShopOrderClient)

    @patch('requests.Session.get')
    def test_establish_connection_unavailable(self, mock_session_get: Mock):
        # Set up the mock session to return a 503 status code
        mock_response = Mock()
        mock_response.status_code = 503
        mock_session_get.return_value = mock_response
        with self.assertRaises(WebServiceUnavailableError):
            PrestaShopOrderClient(self.shop_link, self.api_key)

    @patch('requests.Session.get')
    def test_establish_connection_invalid_api_key(self, mock_session_get: Mock):
        # Set up the mock session to return a 401 status code
        mock_response = Mock()
        mock_response.status_code = 401
        mock_session_get.return_value = mock_response
        with self.assertRaises(InvalidApiKeyError):
            PrestaShopOrderClient(self.shop_link, self.api_key)

    @patch('requests.Session.get')
    def test_establish_connection_unavailable(self, mock_session_get: Mock):
        # Set up the mock session to return a 300 status code
        mock_response = Mock()
        mock_response.status_code = 300
        mock_session_get.return_value = mock_response
        with self.assertRaises(UnexpectedStatusCodeError):
            PrestaShopOrderClient(self.shop_link, self.api_key)

    @patch('requests.Session.get')
    def test_establish_connection_unavailable(self, mock_session_get: Mock):
        mock_session_get.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(PrestaShopConnectionError):
            PrestaShopOrderClient(self.shop_link, self.api_key)
