# Prestashop Orders Client

**Prestashop Orders Client** is a simple client for PrestaShop Api. The main goal of this project is to provide a simple
and easy to use client to interact with PrestaShop Api and to extract either a single order or all orders data. Initially was designed for our own
needs, as we had a big amount of tasks with orders which had to be automated like sending a fresh paid order to our
post service, but we decided to share it with the community. Maybe it will be useful for someone else :)

```
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

*Make sure your server has SSL certificate installed, as PrestaShop Api requires it and our client uses "https" for
performing requests.*

## Installation

Our client available on PyPI:

```console
$ python -m pip install prestashop_orders_client
```

Python 3.10+ is required.

## Important Notes

- Make sure you WebService is enabled in your PrestaShop Admin Panel. (Advanced Parameters -> Webservice)
- Make sure that you have created an Api Key for your WebService. (Advanced Parameters -> Webservice -> Add new key)
- Make sure you have added *GET permissions* at least to these resources : **addresses, countries, customers, orders_states, orders, states**

## License

The project is licensed under the Apache 2.0 License.
