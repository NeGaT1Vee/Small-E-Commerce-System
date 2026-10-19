from models.payment import Payment
from models.cart import Cart
from Enums.enums import OrderStatus
from datetime import date
from models.orderitem import OrderItem  
from exceptions import ValidationError 

class Order():
    def __init__(self, order_id:str , customer_id:str , created_on:date , status:OrderStatus = OrderStatus.PENDING , discount_rate:float = 0.0 , items:list[OrderItem] | None = None, payment:Payment | None =None):
        
        self.order_id = order_id
        self.customer_id = customer_id
        self.created_on = created_on
        self.status = status
        self.discount_rate = discount_rate
        self._items = list(items) if items else []
        self._payment = payment


#-------------------------------------------------------------------
# proparities 
#------------------------------------------------------------------
    @property
    def payment(self):
        return self._payment
    
    @property
    def items(self):
        return list(self._items)

    
    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self,value):
        if not isinstance(value,str):
            raise ValidationError ('order id should be str')
        if not value.strip():
            raise ValidationError ("order id shouldn't be empty")
        self._order_id = value

    @property 
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self,value):
        if not isinstance(value,str):
            raise ValidationError ('customer id should be str')
        if not value.strip():
            raise ValidationError ("customer id shouldn't be empty")
        self._customer_id = value

    @property
    def created_on(self):
        return self._created_on

    @created_on.setter
    def created_on(self,value):
        if not isinstance(value,date):
            raise TypeError ('created on should be date')
        self._created_on = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        if not isinstance(value,OrderStatus):
            raise TypeError ('status should be OrderStatus')
        self._status = value

    @property
    def discount_rate(self):
        return self._discount_rate

    @discount_rate.setter
    def discount_rate(self,value ):
        if not isinstance(value,(float,int)):
            raise TypeError ('discount rate should be float')
        if value < 0 or value > 1:
            raise ValueError ("discount rate should be between 0 and 1")
        self._discount_rate = value

    
    


#------------------------------------------------------------------
# Methods
#------------------------------------------------------------------



    @classmethod
    def from_cart(cls, order_id:str , customer_id:str , cart:Cart):
        order_items = []
        for item in cart.items:
            order_item = OrderItem(item.product , item.quantity , item.product.price)
            order_items.append(order_item)
        return cls(order_id=order_id,customer_id=customer_id,items=order_items,status=OrderStatus.PENDING,discount_rate=0.0,payment=None,created_on=date.today())
        
        
    def total(self):
        sub = sum(item.subtotal() for item in self._items)
        discounted_amount = sub * self.discount_rate
        return max(0.0, sub - discounted_amount)
        


    def apply_discount(self,rate:float):
       self.discount_rate = rate


    def mark_paid(self,payment:Payment):
        
        if not isinstance(payment, Payment):
            raise ValidationError("payment must be a Payment object")
        if self._status != OrderStatus.PENDING:
            raise ValidationError(f"cannot pay an order that is {self._status.value}")
        
        if payment.get_amount() < self.total():
            raise ValueError("Payment amount is less than the order total.")
        if not payment.process():
            raise ValueError("Payment processing failed.")

        for item in self._items:
            if not item.product.is_in_stock(item.quantity):
                raise ValidationError(f"not enough stock for {item.product.name}")

        for item in self._items:
            item.product.reduce_stock(item.quantity)
        
        self._payment = payment
        self._status = OrderStatus.PAID

    def cancel(self):
        if self.status == OrderStatus.CANCELLED:
            raise ValidationError("Order is already cancelled.")
        
        if self._status == OrderStatus.PAID:
            for item in self._items:
                item.product.increase_stock(item.quantity)
        self._status = OrderStatus.CANCELLED



# x = Order(order_id="ORD-001", customer_id="CUS-001", created_on=date.today(), status=OrderStatus.PENDING, discount_rate=0.0, items=[], payment=None)

# print(f"Order ID: {x.order_id}")
# books = Category(category_id="CAT-001", name="Books")
# z = Product("001" , "pen" , 64.5 , 20,books)

# y = OrderItem(z , 5 , 64.5)
# print(f"Order Item Product: {z.name}, Quantity: {y.quantity}, Unit Price: {y.unit_price}, Subtotal: {y.subtotal()}")



# print(x.total([y]))