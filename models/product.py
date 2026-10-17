from exceptions import ValidationError
from models.category import Category


class Product():

    def __init__(self, product_id : str , name : str , price : float , stock :int , category : Category):
            
        if not isinstance(stock , int) or stock < 0:
            raise ValidationError("Stock must be a POSITIVE whole number (integer) only !!")
        
        self._product_id = product_id
        self.name = name
        self.price = price
        self._stock = stock
        self._category = category

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock
    
    @property
    def category(self) -> Category:
        return self._category   
    
    @name.setter
    def name(self , NewName:str):

        if not isinstance(NewName ,str) or not NewName.strip():
            raise ValidationError("Product name cant be empty and must be letters")
        
        self._name = NewName.strip()

    @price.setter
    def price(self , value : float):

        if not isinstance(value,(int,float))  or value <= 0 :
            raise ValidationError("the price must be bigger than zero")    
        self._price = value


    def is_in_stock(self, value:int = 1):
    
        if self._stock >= value:
            return(True)
        return(False)

    def reduce_stock(self , value : int):
        if not isinstance(value,int) or value <=0 :
            raise ValidationError("value must be whole number and bigger than zero")
        
        if value > self._stock:
            raise ValidationError(f"there is only this {self.__stock} number in stock")
        self._stock -= value
        return(f"stock updated to{self._stock}") 

    def increase_stock(self , value):
        if not isinstance(value,int) or value <=0 :
            raise ValidationError("value must be whole number and bigger than zero")
           
        self._stock += value
        return self._stock

    def to_dict(self):
        return {
            "product_id": self._product_id,
            "name": self.name,
            "price": self.price,
            "stock": self._stock,
            "category_id": self._category.category_id
        }


    @classmethod
    def from_dict(cls ,data: dict, categories: dict):
        category = categories.get(data["category_id"])
        if category is None:
            raise ValidationError(f"Category [{data['category_id']}] not found.")
        return cls(data["product_id"], data["name"], data["price"], data["stock"], category)



    ## these are neccessary because in store when using the searchproduct method 
    ## it will give the reuslt as a memory location not the actual answer we want
    def __str__(self) -> str:
        return f"{self._name} - ${self._price:.2f} ({self._stock} in stock)"

    def __repr__(self) -> str:
        return self.__str__()





## test for the product class with its functions :
#x = Product("1001" , "pen" , 248.5 , 20)

#print(x.reduce_stock(7))
#print(x.increase_stock(7))

##books = Category("CAT002", "Books")
#x = Product("1001", "PEN", 2.0, 20, books)

#print(x)                  # PEN - $2.00 (20 in stock)
#x.reduce_stock(5)
#print(x.stock)            # 15
#print(x.to_dict())        # {'product_id': '1001', 'name': 'PEN', ...}


#books = Category("CAT001", "Books")
#toys  = Category("CAT002", "Toys")
#games = Category("CAT003", "Games")

#products = [
 #   Product("1", "Novel",    10.0, 5, books),
  #  Product("2", "Textbook", 30.0, 8, books),
   # Product("3", "Robot",    25.0, 3, toys),
#] 

#print(books.category_id , books.name)
#print("Books:", books.count_products(products))
#books.name =123 #gives error 
#print(books.name) 

