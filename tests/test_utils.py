from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from prestashop_orders_client.exceptions import UnexpectedStatusCodeError, ResourceForbiddenError, \
    PrestaShopConnectionError
from prestashop_orders_client.utils import _get_resource_as_dict


class TestGetResourceAsDict(TestCase):

    @patch('requests.Session')
    def test_successful_response(self, mock_session: Mock):
        # Set up the mock to return a response with an OK status code.
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'<prestashop>' \
                                b'<customer>' \
                                b'<id>123</id>' \
                                b'<email>test@example.com</email>' \
                                b'</customer>' \
                                b'</prestashop>'
        mock_session.get.return_value = mock_response

        # Call the function with a valid link and xml_root
        result = _get_resource_as_dict(mock_session, "https://example.com", "customer")

        # Assert that the function returns the expected result
        self.assertEqual(result, {'id': '123', 'email': 'test@example.com'})

    @patch("requests.Session")
    def test_resource_not_found(self, mock_session: Mock):
        # Set up the mock to return an unsuccessful response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response

        # Call the function with a valid link and xml_root
        result = _get_resource_as_dict(mock_session, "https://example.com", "customer")

        # Assert that the function returns an empty dictionary
        self.assertEqual(result, {})

    @patch("requests.Session")
    def test_unexpected_status_code(self, mock_session: Mock):
        # Set up the mock to return an unsuccessful response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_session.get.return_value = mock_response

        with self.assertRaises(UnexpectedStatusCodeError):
            # Call the function with a valid link and xml_root
            _get_resource_as_dict(mock_session, "https://example.com", "customer")

    @patch("requests.Session")
    def test_resource_forbidden(self, mock_session: Mock):
        # Set up the mock to return an unsuccessful response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_session.get.return_value = mock_response

        with self.assertRaises(ResourceForbiddenError):
            # Call the function with a valid link and xml_root
            _get_resource_as_dict(mock_session, "https://example.com", "customer")

    @patch("requests.Session")
    def test_request_exception(self, mock_session: Mock):
        mock_session.get.side_effect = requests.exceptions.RequestException
        # Assert that the PrestaShopConnectionError exception is raised
        with self.assertRaises(PrestaShopConnectionError):
            _get_resource_as_dict(mock_session, "https://example.com", "customer")
