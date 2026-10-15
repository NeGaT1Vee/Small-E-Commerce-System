class OrderItem:
    def __init__(self,quantity:int,unit_price:float):
        self.__quantity=quantity
        self.__unit_price=unit_price
    #quantity validation
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self,new_quantity):
        if not isinstance(new_quantity,int):
            raise TypeError("quantity must be int")
        else:
            self.quantity=new_quantity
    #unit_price validation
    @property
    def unit_price(self):
            return self.__unit_price
    @unit_price.setter
    def unit_price(self,new_unit_price):
            if not isinstance(new_unit_price,float):
                raise TypeError("unit_price must be float")
            else:
                self.unit_price=new_unit_price
    #subtotal method
    def subtotal(self):
         return self.quantity*self.unit_price