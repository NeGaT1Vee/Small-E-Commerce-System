from models.category import Category
from models.payment import payment
from models.product import Product
from . import cart
from .Enums.enums import OrderStatus
from . import date
from models.orderitem import OrderItem   

class Order():
    def __init__(self,order_id:str,customer_id:str,created_on:date,status:OrderStatus.PENDING,discount_rate:float,items:OrderItem,payment:payment):
        
        self.order_id = order_id
        self.customer_id = customer_id
        self.created_on = created_on
        self.status = status
        self.discount_rate = discount_rate
        self.__items = list(items)
        self.__payment = payment


#-------------------------------------------------------------------
# proparities 
#------------------------------------------------------------------
    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self,value):
        if not isinstance(value,str):
            raise TypeError ('order id should be str')
        if not value.strip():
            raise ValueError ("order id shouldn't be empty")
        self.__order_id = value

    @property 
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self,value):
        if not isinstance(value,str):
            raise TypeError ('customer id should be str')
        if not value.strip():
            raise ValueError ("customer id shouldn't be empty")
        self.__customer_id = value

    @property
    def created_on(self):
        return self.__created_on

    @created_on.setter
    def created_on(self,value):
        if not isinstance(value,date):
            raise TypeError ('created on should be date')
        self.__created_on = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self,value):
        if not isinstance(value,OrderStatus):
            raise TypeError ('status should be OrderStatus')
        self.__status = value

    @property
    def discount_rate(self):
        return self.__discount_rate

    @discount_rate.setter
    def discount_rate(self,value):
        if not isinstance(value,float):
            raise TypeError ('discount rate should be float')
        if value < 0 or value > 1:
            raise ValueError ("discount rate should be between 0 and 1")
        self.__discount_rate = value

    
    


#------------------------------------------------------------------
# Methods
#------------------------------------------------------------------



    @classmethod
    def from_cart(cls,order_id:str,customer_id:str,cart:cart):
        order_items = []
        for item in cart.items:
            order_item = OrderItem(item.product,item.quantity,item.unit_price)
            order_items.append(order_item)
        return cls(order_id=order_id,customer_id=customer_id,items=order_items,status=OrderStatus.PENDING,discount_rate=0.0,payment=None,created_on=date.today())
        
        
    def total(self):
        sub = sum(item.subtotal() for item in self.__items)
        discounted_amount = sub * self.discount_rate
        return max(0.0, sub - discounted_amount)
        


    def apply_discount(self,rate:float):
       self.discount_rate = rate


    def mark_paid(self,payment:payment):
        if payment.get_amount() < self.total():
            raise ValueError("Payment amount is less than the order total.")
        if not payment.process():
            raise ValueError("Payment processing failed.")
        self.__payment = payment
        self.status = OrderStatus.PAID

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        for item in self.__items:
            item.product.increase_stock(item.quantity)




# x = Order(order_id="ORD-001", customer_id="CUS-001", created_on=date.today(), status=OrderStatus.PENDING, discount_rate=0.0, items=[], payment=None)

# print(f"Order ID: {x.order_id}")
# books = Category(category_id="CAT-001", name="Books")
# z = Product("001" , "pen" , 64.5 , 20,books)

# y = OrderItem(z , 5 , 64.5)
# print(f"Order Item Product: {z.name}, Quantity: {y.quantity}, Unit Price: {y.unit_price}, Subtotal: {y.subtotal()}")



# print(x.total([y]))