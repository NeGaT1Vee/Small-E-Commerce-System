from models.product import Product
from models.customer import Customer
from models.category import Category
from models.cart import Cart
from models.CartItem import CartItem
from models.order import Order

class Store:
    def __init__(self, products: list[Product], customers: list[Customer], categories: list[Category]):
        self.__products = products
        self.__customers = customers
        self.__categories = categories

    @property
    def products(self):
        return self.__products

    @property
    def customers(self):
        return self.__customers

    @property
    def categories(self):
        return self.__categories
    
    def add_product(self, p: Product):
     for existing_product in self.__products:
        if existing_product.product_id == p.product_id:
            raise ValueError("Product is already in products")
            
     self.__products.append(p)

    def search_products(self, keyword: str):
        keyword = keyword.lower()
        return [product for product in self.__products if keyword in product.name.lower()]

    def add_to_cart(self, cid: str, pid: str, qty: int):
        customer = next((c for c in self.__customers if c.customer_id == cid), None)
        if not customer:
            raise ValueError("Customer not found")
        
        product = next((p for p in self.__products if p.product_id == pid), None)
        if not product:
            raise ValueError("Product not found")
        
        if not product.is_in_stock(qty):
            raise ValueError("Not enough stock available")
        
        customer.cart.add_item(product, qty)

    def checkout(self, cid: str, method: str):
        customer = next((c for c in self.__customers if c.customer_id == cid), None)
        if not customer:
            raise ValueError("Customer not found")
        
        if not customer.cart.items:
            raise ValueError("Cart is empty")
        
        for item in customer.cart.items:
            item.product.reduce_stock(item.quantity)
        
        order = Order(customer=customer, items=customer.cart.items, payment_method=method)
        customer.cart.clear()
        return order

    def dashboard_stats(self):
        return {
            "total_products": len(self.__products),
            "total_customers": len(self.__customers),
            "total_categories": len(self.__categories)
        }