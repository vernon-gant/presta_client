# PrestaShop Orders Client

**PrestaShop Orders Client** is a simple, thoroughly tested client for the PrestaShop API designed to extract order data seamlessly. Initially created to meet our automation needs for tasks such as sending fresh paid orders to our postal service, we decided to share this easy-to-use client with the community. We hope it proves useful to others as well!

```python
>>> from prestashop_orders_client import PrestaShopOrderClient
>>> client = PrestaShopOrderClient(shop_link="myshop.com", api_key="my_api_key")
>>> client.get_order(1)
Order(id=1, total_paid=500.0, reference='ABCD'
      order_state='Shipped', email='examplemail@gmail.com', 
      first_name='John', last_name='Doe', 
      company_name=None, phone='+12345678', 
      address='Example address', 
      city='Example city', post_code='123456', 
      country='Example country', state=None)
>>> client.get_all_orders()
[
Order(id=1, total_paid=500.0, reference='ABCD'
      order_state='Shipped', email='examplemail@gmail.com', 
      first_name='John', last_name='Doe', 
      company_name=None, phone='+12345678', 
      address='Example address', 
      city='Example city', post_code='123456', 
      country='Example country', state=None),

Order(id=2, total_paid=1000.0, reference='ABCD'
      order_state='Shipped', email='examplemail@gmail.com', 
      first_name='John', last_name='Doe', 
      company_name=None, phone='+12345678', 
      address='Example address', 
      city='Example city', post_code='123456', 
      country='Example country', state=None),
....
]
>>> client.orders_amount
8
```

*Ensure your server has an SSL certificate installed, as the PrestaShop API requires it, and our client uses "https" for performing requests.*

## Installation

The client is available on PyPI and requires Python 3.10+

```console
$ python -m pip install prestashop_orders_client
```

## Important Notes

- Ensure the WebService is enabled in your PrestaShop Admin Panel (Advanced Parameters -> Webservice).
- Create an API Key for your WebService (Advanced Parameters -> Webservice -> Add new key).
- Grant GET permissions to these resources at a minimum : **addresses, countries, customers, orders_states, orders, states**

## License

The project is licensed under the Apache 2.0 License.
