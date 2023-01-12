"""
prestashop_orders_client.client
~~~~~~~~~~~~~~
This module provides main functionality of our package. It contains class that is used to communicate with PrestaShop
API and retrieve orders.
"""
import requests

from .exceptions import *
from .parser import _OrderParser
from .utils import _get_resource_as_dict, Order


class PrestaShopOrderClient:
    """
    A client for interacting with the PrestaShop orders API.
    This class allows you to establish a connection to the PrestaShop API,
    retrieve information about orders and parse them to the Order object.
    """

    def __init__(self, shop_link: str, api_key: str):
        """
        Initializes the client with the provided shop link and API key.

        :param shop_link: The link of the shop to connect to.
        :param api_key: The API key to use for authentication.
        :raises: InvalidApiKeyError, WebServiceUnavailableError, UnexpectedStatusCodeError, PrestaShopConnectionError
        """
        self.__shop_api_url = "https://{}/api".format(shop_link)
        self.__session = self.__establish_connection(api_key)
        self.__order_parser = _OrderParser(self.__session)
        self.orders_amount = self.__count_orders()

    def __establish_connection(self, api_key: str) -> requests.Session:
        """
        Establishes a connection to the API and returns the session object.
        :param api_key: The API key to use for authentication.
        :return: session object
        :raises: InvalidApiKeyError, WebServiceUnavailableError, UnexpectedStatusCodeError, PrestaShopConnectionError
        """
        with requests.Session() as presta_client:
            presta_client.auth = (api_key, "")
            try:
                test_response = presta_client.get(self.__shop_api_url)
                if test_response.status_code == 200:
                    return presta_client
                elif test_response.status_code == 503:
                    raise WebServiceUnavailableError(
                        "WebService Api is unavailable! Turn it on in your shop settings.")
                elif test_response.status_code == 401:
                    raise InvalidApiKeyError("Invalid API key!")
                else:
                    raise UnexpectedStatusCodeError(
                        f"Unexpected status code: {test_response.status_code}\nError: {test_response.text}")
            except requests.RequestException as e:
                raise PrestaShopConnectionError("Could not connect to the server!\n{}".format(e))

    def __count_orders(self) -> int:
        """
        Counts the number of orders available in the shop.
        :return: int
        :raises: OrdersNotFound
        """
        orders_list = _get_resource_as_dict(self.__session, "{}/orders".format(self.__shop_api_url), "orders").get(
            'order')
        if orders_list:
            return len(orders_list)
        else:
            raise OrdersNotFound("No orders found! Add some to your shop.")

    def get_all_orders(self) -> list[Order]:
        """
        Retrieve a list of all orders present in the shop.

        Returns:
            A list of Order objects, representing all orders present in the shop.
        """
        return [self.get_order(i) for i in range(1, self.orders_amount + 1)]

    def get_order(self, number: int) -> Order:
        """
        Retrieve a specific order by its number.

        Args: number (int): The order number to retrieve. Must be greater than or equal to 1 and less than or equal
        to the total number of orders.

        Returns:
            An Order object representing the order with the specified number.

        Raises:
            InvalidOrderNumber: if the provided number is not a valid order number.
        """
        if number < 1 or number > self.orders_amount:
            raise InvalidOrderNumber(f"Invalid order number! Must be >= 1 and <= {self.orders_amount}")
        order_link = f"{self.__shop_api_url}/orders/{number}"
        return self.__order_parser.parse_order(order_link)
