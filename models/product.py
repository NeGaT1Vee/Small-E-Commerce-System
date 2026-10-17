class Product:
    def __init__(self,product_id:str,name:str,price:float,stock:int):
        self.__product_id=product_id
        self.__name=name
        self.__price=price
        self.__stock=stock
    #product_id validation
    @property
    def product_id(self):
        return self.product_id
    @product_id.setter
    def product_id(self,id):
        if not isinstance(id,str):
            raise TypeError("id must to be string")
        else:
            self.product_id=id
    #name validation
    @property
    def name(self):
            return self.name
    @name.setter
    def name(self,new_name):
            if not isinstance(new_name,str):
                raise TypeError("name must to be string")
            else:
                self.name=new_name
    #price validation
    @property
    def price(self):
         return self.price
    @price.setter
    def price(self,new_price):
        if not isinstance(new_price,(int,float)):
              raise TypeError("price must be int or float")
        else:
             new_price=self.price
    #stock validation
    @property
    def stock(self):
             return self.price
    @stock.setter
    def price(self,new_stock):
            if not isinstance(new_stock,(int)):
                  raise TypeError("stock must be int")
            else:
                 new_stock=self.stock
    