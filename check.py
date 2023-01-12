from prestashop_orders_client import

client = PrestaShopOrderClient("shop.levus.co/LVS", "3Z7TUAA1CZC5PCIXTJKGAE5YU83RHGKK")

print(client.get_order(201))