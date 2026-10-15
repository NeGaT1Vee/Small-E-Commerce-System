from src.models.Enums.enums import orderstatus
from src.models.Entities import OrderItem
from datetime import date
class Order:
    def __init__(self,order_id:str,created_on:date,discount_rate:float,order_items:list[OrderItem],status:orderstatus=orderstatus.PENDING):
        self.order_id=order_id
        self.created_on=created_on
        self.discount_rate=discount_rate
        self.status=status
        self.order_items=order_items

    @property
    def order_id(self):
            return self.__order_id
    @order_id.setter
    def order_id(self,id):
                if not isinstance(id,str):
                    raise TypeError("id must to be string")
                if not id.strip():
                    raise ValueError("id is empty")
                else:
                    self.__order_id=id

    @property
    def created_on(self):
             return self.__created_on
    @created_on.setter
    def created_on(self,on_date):
             if not isinstance(on_date,date):
                  raise TypeError("enter a valid date")
             self.__created_on=on_date

    @property
    def order_items(self):
        return self.__order_items
        
    @order_items.setter
    def order_items(self, items):
        if not isinstance(items, list):
            raise TypeError("order_items must be a list")
        for item in items:
            if not isinstance(item, OrderItem):
                raise TypeError("each item must be of type OrderItem")
        self.__order_items = items

    @property
    def discount_rate(self):
          return self.__discount_rate
    @discount_rate.setter
    def discount_rate(self,rate):
        if not isinstance(rate,float):
              raise TypeError("rate must be a float")
        if not (0.0 <= rate <= 1.0):
            raise ValueError("rate must be between 0.0 and 1.0")
        self.__discount_rate=rate

    @property
    def status(self):
          return self.__status
    @status.setter
    def status(self,new_status):
        if not isinstance(new_status,orderstatus):
              raise TypeError("enter a valid status")
        self.__status=new_status 
    #methods:-
    #1-total
    def total(self):
        total=0
        for item in self.__order_items:
            total+=item.subtotal()
        if self.__discount_rate>0:
              total-=total*self.__discount_rate
        return total
    #2-apply_discount
    def apply_discount(self,rate):
        if not isinstance(rate,float):
            raise TypeError("rate must be a float")
        if not (0.0 <= rate <= 1.0):
            raise ValueError("rate must be between 0.0 and 1.0")
        self.__discount_rate=rate   
    #3-cancel
    def cancel(self):
          self.__status=orderstatus.CANCELED