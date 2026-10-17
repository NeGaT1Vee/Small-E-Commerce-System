from models.product import Product
from exceptions import ValidationError


class OrderItem():
    def __init__(self , product : Product , quantity : int , unit_price : float):
        
        if not isinstance(product , Product):
            raise ValidationError("order item needs a product")
        
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("Quantity must be a whole number greater than zero.")
        
        self._product = product
        self._quantity = quantity
        self._unit_price = unit_price

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity 

    @property
    def unit_price(self):
        return self._unit_price  


    def subtotal(self):

        return self.unit_price * self.quantity    

    ## x = Product("001" , "pen" , 64.5 , 20 , books)
    # y = OrderItem(x , 5 , product.price)