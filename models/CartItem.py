from models.product import Product
class CartItem:
    def __init__(self,quantity:int,product:Product):
        self.quantity=quantity
        self.__product=product
    #quantity validation
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self,new_quantity):
        if not isinstance(new_quantity,int):
            raise TypeError("quantity must be int")
        if new_quantity<=0:
            raise ValueError("quantity must be greater than 0")
        else:
            self.__quantity=new_quantity
    #subtotal method
    def subtotal(self):
        return self.__quantity*self.__product.price