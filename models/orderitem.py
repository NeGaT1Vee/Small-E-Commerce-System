from models.product import Product
from exceptions import ValidationError


class OrderItem():
    def __init__(self , product : Product , quantity : int , unit_price : float):
        
        if not isinstance(product , Product):
            raise ValidationError("order item needs a product")
        
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("Quantity must be a whole number greater than zero.")
        
        self.__product = product
        self.__quantity = quantity
        self.__unit_price = unit_price


    def subtotal(self):

        return self.__unit_price * self.__quantity    