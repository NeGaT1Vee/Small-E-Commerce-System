from models.product import Product
from models.customer import Customer
from models.category import Category
from models.order import Order
from file_manager.file_manager import FileManager


class Store:
    def __init__(self, customer: list[Customer], product: list[Product], category: list[Category], order: list[Order], file_manager: FileManager):
        self.__customer = list(customer)
        self.__product = list(product)
        self.__category = list(category)
        self.__order = list(order)
        self.__file_manager = file_manager

    @property
    def customer(self):
        return self.__customer

    @property
    def product(self):
        return self.__product

    @property
    def category(self):
        return self.__category 

    @property
    def order(self):
        return self.__order

    @property
    def file_manager(self):
        return self.__file_manager

#---------------------------------------------------
# Methods Products
# ---------------------------------------------------

    def add_product (self, product: Product):
        if product.product_id in [p.product_id for p in self.__product]:
            raise ValueError(f"Product with ID {product.product_id} already exists.")
        self.__product.append(product)
        self.__file_manager.save_products(self.__product)

    def update_product(self, product_id: str, updated_product: Product):
        for i, product in enumerate(self.__product):
            if product.product_id == product_id:
                self.__product[i] = updated_product
                self.__file_manager.save_products(self.__product)
                return
        raise ValueError(f"Product with ID {product_id} not found.")

    def delete_product(self, product_id: str):
        for i, product in enumerate(self.__product):
            if product.product_id == product_id:
                del self.__product[i]
                self.__file_manager.save_products(self.__product)
                return
        raise ValueError(f"Product with ID {product_id} not found.")

    def get_product(self, product_name: str) -> Product:
        for product in self.__product:
            if product.product_name == product_name:
                return product
        raise ValueError(f"Product with name {product_name} not found.")

#---------------------------------------------------
# Methods Customers
#---------------------------------------------------




#---------------------------------------------------
#Methods Cart & chickout
#---------------------------------------------------

    
    