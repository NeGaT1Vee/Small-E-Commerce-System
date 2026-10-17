from abc import ABC,abstractmethod
from datetime import date,time
class Payment(ABC):
    def __init__(self,payment_id:str,amount:float,paid_on:date):
        self.payment_id=payment_id
        self.amount=amount
        self.paid_on=paid_on

    @property
    def payment_id(self):
        return self.__payment_id
    @payment_id.setter
    def payment_id(self,new_id):
        if not isinstance(new_id,str):
            raise TypeError("id must be a string")
        if not new_id.strip():
            raise ValueError("id mustn't be empty")
        self.__payment_id=new_id

    @property
    def amount(self):
            return self.__amount
    @amount.setter
    def amount(self,new_amount):
            if not isinstance(new_amount,(int,float)):
                raise TypeError("amount must be a float")
            if new_amount<=0:
                raise ValueError("invalid amount")
            self.__amount=new_amount

    @property
    def paid_on(self):
         return self.__paid_on
    @paid_on.setter
    def paid_on(self,new_date):
        if not isinstance(new_date,date):
            raise TypeError("paid_on must be a date")
        if not str(new_date).strip():
            raise ValueError("paid on is empty")
        if new_date > date.today():
            raise ValueError("Payment date cannot be in the future")
        self.__paid_on=new_date
    #methods:-
    #1-process:-
    @abstractmethod
    def process(self):
        pass

    def get_amount(self):
         return self.__amount    