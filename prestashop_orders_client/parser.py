"""
prestashop_orders_client.parser
~~~~~~~~~~~~~~
This module provides a class that parses order data from PrestaShop API. It is used by PrestaShopOrderClient class.
Made not to be used by external users.
"""
import requests

from .utils import Order, _get_resource_as_dict, ORDER_COMPONENTS


class _OrderParser:
    """
    A class used to parse order data from PrestaShop API and return it as an Order object.
    """

    def __init__(self, session: requests.Session):
        """
        Initializes an instance of the OrderParser class

        :param session: A requests.Session object used to make API requests.
        """
        self.session = session

    def parse_order(self, order_link: list) -> Order:
        """
        Parses an order from the provided order link and returns it as an Order object

        :param order_link: A link to the order resource.
        :return: An Order object.
        """
        ready_order, order_data = dict(), self.extract_order_data(order_link)
        for resource, data in order_data.items():
            ready_order |= self.parse_resource(resource, data)
        return Order(**ready_order)

    def extract_order_data(self, order_link: str) -> dict:
        """
        Extracts all the necessary data for the order from the API

        :param order_link: A link to the order resource.
        :return: A dictionary containing all the necessary data for the order.
        """
        order_data = _get_resource_as_dict(self.session, order_link, "order")
        order_state_data = _get_resource_as_dict(self.session, order_data['current_state']['@xlink:href'],
                                                "order_state")
        customer_data = _get_resource_as_dict(self.session, order_data['id_customer']['@xlink:href'], "customer")
        address_data = _get_resource_as_dict(self.session, order_data['id_address_delivery']['@xlink:href'],
                                            "address")
        country_data = _get_resource_as_dict(self.session, address_data['id_country']['@xlink:href'], "country")
        try:
            state_data = _get_resource_as_dict(self.session, address_data['id_state']['@xlink:href'], "state")
        # If state is not set(there will be '0' in state field
        # ->
        # accessing it like a dict will produce TypeError),
        # state_data will be empty dict
        except TypeError:
            state_data = {}
        return {resource: data for resource, data in zip(ORDER_COMPONENTS,
                                                         [order_data, order_state_data, customer_data, address_data,
                                                          country_data,
                                                          state_data])}

    @staticmethod
    def parse_resource(resource: str, data: dict) -> dict:
        """
        Parses the provided resource data and returns it as a dictionary

        :param resource: The resource name.
        :param data: The data for the resource.
        :return: A dictionary containing the parsed data.
        """
        orders_part = dict()
        match resource:
            case "order":
                orders_part.__setitem__("id", int(data.get("id")))
                orders_part.__setitem__("total_paid", float(data.get("total_paid")))
                orders_part.__setitem__("reference", data.get("reference"))
            case "order_state":
                orders_part.__setitem__("order_state",
                                        data.get("name").get("language").get(
                                            "#text"))
            case "customer":
                orders_part.__setitem__("email", data.get("email"))
            case "address":
                orders_part.__setitem__("first_name", data.get("firstname"))
                orders_part.__setitem__("last_name", data.get("lastname"))
                orders_part.__setitem__("company_name", data.get("company"))
                orders_part.__setitem__("phone", data.get("phone"))
                orders_part.__setitem__("address", data.get("address1") + (" " + data.get("address2") if data.get(
                    "address2") is not None else ""))
                orders_part.__setitem__("city", data.get("city"))
                orders_part.__setitem__("post_code", data.get("postcode"))
            case "country":
                orders_part.__setitem__("country",
                                        data.get("name").get("language").get("#text"))
            case "state":
                orders_part.__setitem__("state", data.get("name"))
        return orders_part
