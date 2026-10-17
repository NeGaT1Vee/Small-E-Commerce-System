from models.category import Category
from models.customer import Customer
from models.product import Product
from store.store import Store
from file_manager.file_manager import FileManager   # adjust to your real file name

books = Category("CAT001", "Books")
pen = Product("1", "Pen", 2.5, 10, books)
alice = Customer("C1", "Alice", "alice@gmail.com", "0100000000")
store = Store([alice], [pen], [books])

fm = FileManager("data")
fm.save_store(store)

loaded = fm.load_store()
for product in loaded.products:
    print(product)