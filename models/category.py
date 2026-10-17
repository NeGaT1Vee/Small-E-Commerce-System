from models.product import Product
class Category:
    def __init__(self, name: str, category_id: str):
        name = name.strip()
        if not name:
            raise ValueError("Category name is required.")
        self._category_id = category_id
        self._name = name
        self._products: list[Product] = []

    @property
    def category_id(self):
        return self._category_id

    @property
    def name(self):
        return self._name

    @property
    def products(self):
        return list(self._products)

    def add_product(self, product: Product):
        if product not in self._products:
            self._products.append(product)

    def count_products(self):
        return len(self._products)
    