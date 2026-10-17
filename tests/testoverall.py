from models.category import Category
from models.product import Product
from models.cartitem import CartItem
from models.orderitem import OrderItem
from exceptions import ValidationError
from store.store import Store
from models.customer import Customer




categories = [
    Category("CATEGORY 001" , "Books"),
    Category("CATEGORY 002" , "Pens"),
    Category("CATEGORY 003" , "Clothes")
]

products = [
    Product("1", "Novel",    10.0, 5, categories[0]),
    Product("2", "Textbook", 30.0, 8, categories[0]),
    Product("3", "Pencil",    25.0, 3, categories[1]),
] 

customers = [
    Customer("ID 22", "amr",  "amr@gmail.com",  "01087654271"),
    Customer("ID 23", "sara", "sara@gmail.com", "01011112222"),
    Customer("ID 24", "omar", "omar@gmail.com", "01255556666"),
]


#cartitem1 = CartItem(products[2] , 5)
#print(cartitem1.product.name, cartitem1.quantity)
#print(cartitem1.subtotal())

#orderitem1 = OrderItem(products[2] , cartitem1.quantity , cartitem1.product.price)
#print(orderitem1.subtotal())

test_store = Store(customers , products , categories )
print(len(test_store.products))
new_product = Product("4" , "t-shirt" , 60.5 , 12 , categories[2])
test_store.add_product(new_product)
print(len(test_store.products))

print(test_store.search_products("pencil"))