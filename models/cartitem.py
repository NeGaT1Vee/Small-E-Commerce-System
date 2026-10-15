from models.product import Product
from exceptions import ValidationError
from models.category import Category




class CartItem():

    def __init__(self , product : Product , quantity : int):

        if not isinstance(product , Product):
            raise ValidationError("the cart is empty , please fill it") 

        self._product = product
        self.quantity = quantity


    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self , value : int):
        if not isinstance(value , int) or value <= 0 :
            raise ValidationError("the quantity must be a whole number and greated than zero")  

        self._quantity = value


    def subtotal(self):

        return self._product.price * self._quantity


