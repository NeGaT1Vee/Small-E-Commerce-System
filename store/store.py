from models.product import Product
from models.customer import Customer
from models.category import Category
from exceptions import ValidationError
from models.cart import Cart
from models.order import Order
from models.payment import  Payment , CardPayment , CashPayment
from datetime import date
from Enums.enums import OrderStatus

class Store():
    def __init__(self , customers : list[Customer] , products : list[Product] , categories : list[Category]):
        if not isinstance(customers , list):
            raise ValidationError("you must put a list of customers!")
        if not isinstance(products , list):
            raise ValidationError("you must put a list of products!")
        if not isinstance(categories , list):
            raise ValidationError("you must put a list of categories!")
        self._customers = customers
        self._products = products
        self._categories = categories
        self._orders = []
        
    @property
    def customers(self):
        return list(self._customers)
    @property
    def products(self):
        return list(self._products)
    @property
    def categories(self):
        return list(self._categories)
    @property
    def orders(self):
        return list(self._orders)

    def add_category(self, new_category: Category):
        if not isinstance(new_category, Category):
            raise ValidationError("you must add a valid category")
        for category in self._categories:
            if category.category_id == new_category.category_id:
                raise ValidationError("a category with this id already exists")
        self._categories.append(new_category)

    def add_customer(self, new_customer: Customer):
        if not isinstance(new_customer, Customer):
            raise ValidationError("you must add a valid customer")
        for customer in self._customers:
            if customer.customer_id == new_customer.customer_id:
                raise ValidationError("a customer with this id already exists")
        self._customers.append(new_customer)    


    def add_product(self, NewProduct : Product):
        if not isinstance(NewProduct , Product):
            raise ValidationError("you must add a valid product")
        return self._products.append(NewProduct)

    def search_products(self, keyword: str):
        if not isinstance(keyword, str):
            raise ValidationError("the keyword must be string")

        keyword = keyword.strip().lower()
        results = []
        for product in self._products:
            if keyword in product.name.lower():
                results.append(product)
        return results


    ##------------------------------------------------------------
    ## two functions used in add_to_cart function
    def _find_customer(self, cid: str):
        for customer in self._customers:
            if customer.customer_id == cid:
                return customer
        raise ValidationError(f"Customer '{cid}' not found.")

    def _find_product(self, pid: str):
        for product in self._products:
            if product.product_id == pid:
                return product
        raise ValidationError(f"Product '{pid}' not found.")



    def add_to_cart(self , cid : str , pid : str , qty : int):

        customer = self._find_customer(cid)
        product = self._find_product(pid)
        customer.cart.add_item(product , qty)   
    ##-------------------------------------------------------------


    def checkout(self , cid : str , method : str , discount_rate=0.0):

        customer = self._find_customer(cid)
        cart = customer.cart

        if cart.is_empty():
            raise ValidationError("cart cannot be empty")

        order_id = f"ORD-{len(self._orders) + 1:03}"
        order = Order.from_cart(order_id , cid , cart )
        order.apply_discount(discount_rate)
        total = float(order.total())
        if method == "card":
            payment = CardPayment(f"PAY-{order_id}", total, date.today(), "0000")
        elif method == "cash":
            payment = CashPayment(f"PAY-{order_id}", total, date.today(), total)
        else:
            raise ValidationError("method must be 'card' or 'cash'")


        order.mark_paid(payment)
        customer.add_order(order)
        self._orders.append(order)

        cart.clear()
        return order


    def dashboard_status(self):
        paid_orders = []
        
        for order in self._orders:
            if order.status == OrderStatus.PAID :
                paid_orders.append(order)

        today_orders = 0
        for order in self._orders:
            if order.created_on ==date.today():
                today_orders += 1

        total_sales = 0

        for order in paid_orders:
            total_sales += order.total()   

        return {
            "customers" : len(self._customers),
            "products" : len(self._products),
            "total_sales" : total_sales,
            "today_orders" : today_orders
            
        }                 