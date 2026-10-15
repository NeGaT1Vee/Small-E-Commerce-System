from .Enums.enums import OrderStatus
from . import date
from . import orderitem , payment

class orders (order_item,pyment):
    def __init__(self,order_id:str,customer_id:str,created_on:date,status:OrderStatus.PENDING,discount_rate:float,items:orderitem,payment:payment):
        
        super().__init__()
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




        def from_cart(self,order_id:str,customer_id:str,cart:cart):
            pass

        def total():
            pass

        def apply_discount(self,rate:float):
            pass

        def mark_paid(payment:payment):
            pass

        def cancel():
            pass