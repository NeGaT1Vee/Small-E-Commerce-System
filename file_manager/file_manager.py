import json
import os

from exceptions import ValidationError
from models.category import Category
from models.customer import Customer
from models.product import Product


class FileManager:
    """Saves and loads store data as JSON files in one folder."""

    def __init__(self, folder="data"):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

    # ---------- basic read / write ----------
    def write_file(self, filename, data):
        path = os.path.join(self.folder, filename)
        file = open(path, "w")
        json.dump(data, file, indent=2)
        file.close()

    def read_file(self, filename):
        path = os.path.join(self.folder, filename)
        if not os.path.exists(path):
            return []
        file = open(path, "r")
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            file.close()
            raise ValidationError(filename + " is not valid JSON")
        file.close()
        return data

    # ---------- categories ----------
    def save_categories(self, categories):
        data = []
        for category in categories:
            data.append({"category_id": category.category_id, "name": category.name})
        self.write_file("categories.json", data)

    def load_categories(self):
        categories = []
        for item in self.read_file("categories.json"):
            categories.append(Category(item["category_id"], item["name"]))
        return categories

    # ---------- products ----------
    def save_products(self, products):
        data = []
        for product in products:
            data.append(product.to_dict())
        self.write_file("products.json", data)

    def load_products(self, categories):
        # dictionary: category id -> Category object
        category_dict = {}
        for category in categories:
            category_dict[category.category_id] = category

        products = []
        for item in self.read_file("products.json"):
            products.append(Product.from_dict(item, category_dict))
        return products

    # ---------- customers (cart and order history are not saved) ----------
    def save_customers(self, customers):
        data = []
        for customer in customers:
            data.append({
                "customer_id": customer.customer_id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
            })
        self.write_file("customers.json", data)

    def load_customers(self):
        customers = []
        for item in self.read_file("customers.json"):
            customers.append(Customer(item["customer_id"], item["name"],
                                      item["email"], item["phone"]))
        return customers

    # ---------- orders (saved as a record only) ----------
    def save_orders(self, orders):
        data = []
        for order in orders:
            items = []
            for item in order.items:
                items.append({
                    "product_id": item.product.product_id,
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                })

            payment = None
            if order.payment is not None:
                payment = {
                    "type": type(order.payment).__name__,
                    "payment_id": order.payment.payment_id,
                    "amount": order.payment.amount,
                    "paid_on": order.payment.paid_on.isoformat(),
                }

            data.append({
                "order_id": order.order_id,
                "customer_id": order.customer_id,
                "created_on": order.created_on.isoformat(),
                "status": order.status.value,
                "discount_rate": order.discount_rate,
                "items": items,
                "total": order.total(),
                "payment": payment,
            })
        self.write_file("orders.json", data)

    # ---------- whole store ----------
    def save_store(self, store):
        self.save_categories(store.categories)
        self.save_products(store.products)
        self.save_customers(store.customers)
        self.save_orders(store.orders)

    def load_store(self):
        from store.store import Store
        categories = self.load_categories()
        products = self.load_products(categories)
        customers = self.load_customers()
        return Store(customers, products, categories)
