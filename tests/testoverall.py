from models.category import Category
from models.product import Product
from models.cartitem import CartItem
from models.orderitem import OrderItem
from exceptions import ValidationError


books = Category("CATEGORY 001" , "Books")
pens = Category("CATEGORY 002" , "Pens")

products = [
    Product("1", "Novel",    10.0, 5, books),
    Product("2", "Textbook", 30.0, 8, books),
    Product("3", "Pencil",    25.0, 3, pens),
] 

cartitem1 = CartItem(products[2] , 5)
print(cartitem1.product.name, cartitem1.quantity)
print(cartitem1.subtotal())

orderitem1 = OrderItem(products[2] , cartitem1.quantity , cartitem1.product.price)
print(orderitem1.subtotal())