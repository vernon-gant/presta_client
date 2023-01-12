"""
prestashop_orders_client.utils
~~~~~~~~~~~~~~
This module provides utility functions, data structures that are used within our package
that are also useful for external consumption.
"""
from collections import namedtuple

import requests
import xmltodict

from .exceptions import ResourceForbiddenError, UnexpectedStatusCodeError, PrestaShopConnectionError


"""
Representation of an order, containing relevant information about the order.
"""
Order = namedtuple("Order",
                   "id total_paid reference "
                   "order_state "
                   "email "
                   "first_name last_name company_name phone address city post_code "
                   "country "
                   "state")

ORDER_COMPONENTS = ("order", "order_state", "customer", "address", "country", "state")


def _get_resource_as_dict(session: requests.Session, link: str, xml_root: str) -> dict:
    """
    Fetches the given resource from the PrestaShop server and returns it as a dictionary.

    :param session: An active session with the PrestaShop server.
    :param link: The URL of the resource to be fetched.
    :param xml_root: The root element of the resource in the XML response.
    :return: The resource as a dictionary.
    :raises ResourceForbiddenError: If the user doesn't have permission to access the resource.
    :raises UnexpectedStatusCodeError: If the server returns a status code other than 200 or 401.
    :raises PrestaShopConnectionError: If there is an error connecting to the server.
    """
    try:
        response = session.get(link)
        if response.status_code == 200:
            return xmltodict.parse(response.content).get("prestashop").get(xml_root)
        elif response.status_code == 401:
            raise ResourceForbiddenError(
                f"You don't have permission to access {xml_root}! Set correct API key or add it to current ApiKey's "
                f"permission list.")
        elif response.status_code == 404:
            return dict()
        else:
            raise UnexpectedStatusCodeError(
                f"Unexpected status code: {response.status_code}\nError: {response.text}")
    except requests.exceptions.RequestException as e:
        raise PrestaShopConnectionError("Could not connect to the server!\n{}".format(e))
