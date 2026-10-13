from exceptions import ValidationError



class Product():

    def __init__(self, product_id : str , name : str , price : float , stock :int):
            
        if not isinstance(stock , int) or stock < 0:
            raise ValidationError("Stock must be a POSITIVE whole number (integer) only !!")
        
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock


    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    @name.setter
    def name(self , NewName:str):

        if not isinstance(NewName ,str) or not NewName.strip():
            raise ValidationError("Product name cant be empty and must be letters")
        
        self.__name = NewName.strip()

    @price.setter
    def price(self , value : float):

        if value <= 0 :
            raise ValidationError("the price must be bigger than zero")    
        self.__price = value


    def is_in_stock(self, value):
    
        if self.__stock >= value:
            return(True)
        return(False)

    def reduce_stock(self , value):

        self.__stock -= value
        return(self.__stock) 

    def increase_stock(self , value):
    
            self.__stock += value
            return(self.__stock)


x = Product("1001" , "pen" , 248.5 , 20)

print(x.reduce_stock(7))
print(x.increase_stock(7))