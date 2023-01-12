class OrdersNotFound(Exception):
    """An exception raised when there are no orders found in the shop.
    """
    pass


class InvalidOrderNumber(Exception):
    """An exception raised when an invalid order number is provided.
    """
    pass


class InvalidApiKeyError(Exception):
    """An exception raised when an invalid API key is provided.
    """
    pass


class PrestaShopConnectionError(Exception):
    """An exception raised when there is an error connecting to the PrestaShop server.
    """
    pass


class UnexpectedStatusCodeError(Exception):
    """An exception raised when the server returns an unexpected status code.
    """
    pass


class ResourceForbiddenError(Exception):
    """An exception raised when the server returns a '401 Unauthorized' status code.
    """
    pass


class WebServiceUnavailableError(Exception):
    """An exception raised when the server returns a '503 Service Unavailable' status code.
    """
    pass
