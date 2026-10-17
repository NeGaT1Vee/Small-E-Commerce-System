from models.cart import Cart


class Customer:
    def __init__(self,customer_id:str,name:str,email:str,phone:str , ):
        self.customer_id=customer_id
        self.name=name
        self.email=email
        self.phone=phone
        self._orders:list=[]
        self._cart = Cart([])

    @property
    def cart(self):
         return self._cart


    @property
    def customer_id(self):
        return self.__customer_id

    
    @customer_id.setter
    def customer_id(self,cid):
        if not isinstance(cid,str):
                raise TypeError("cid must be string")
        if not cid.strip():
            raise ValueError("cid is empty")
        self.__customer_id=cid

    @property
    def name(self):
            return self.__name

    
    @name.setter
    def name(self,new_name):
            if not isinstance(new_name,str):
                    raise TypeError("name must be string")
            if not new_name.strip():
                raise ValueError("name is empty")
            self.__name=new_name

    @property
    def email(self):
        return self.__email

    
    @email.setter
    def email(self,new_email):
                if not isinstance(new_email,str):
                        raise TypeError("email must be string")
                if not new_email.strip():
                    raise ValueError("email is empty")
                if not "@gmail.com" in new_email:
                      raise ValueError("invalid email")
                self.__email=new_email

    @property
    def phone(self):
        return self.__phone

    
    @phone.setter
    def phone(self,new_phone):
        if not isinstance(new_phone,str):
            raise TypeError("phone must be string")
        if not new_phone.strip():
            raise ValueError("phone is empty")
        self.__phone=new_phone
    
    #methods
    #1-add order
    def add_order(self,order):
         self._orders.append(order)


    #2-order history
    def order_history(self):
          return self._orders



    #3-__str__
    def __str__(self):
     return f"Customer(ID: {self.customer_id}, Name: {self.name}, Email: {self.email}, Phone: {self.phone})"