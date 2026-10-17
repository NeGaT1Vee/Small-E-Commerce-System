''' payment here is abstract , it always should be'''
from abc import ABC, abstractmethod
from datetime import date
class Payment(ABC):
    
    '''abstract class init'''

    def __init__(self,payment_id:str,amount:float,paid_on: date ):
        self.payment_id = payment_id
        self.amount = amount 
        self.paid_on = paid_on


#_____________________________________________________________________________________________________
# proparites and sitters for arg (encapsualtion and validation)
#_____________________________________________________________________________________________________
    @property
    def payment_id(self):
        return self._payment_id

    @payment_id.setter
    def payment_id(self,value):
        if not isinstance(value,str):
            raise TypeError('payment id has to be str')
        if not value.strip():
            raise ValueError("payment id can't be empty")

        self._payment_id = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self,value):
        if not isinstance(value,(int,float)):
            raise TypeError('amount has to be a number')
        if value <0 :
            raise ValueError("value can't be below 0")
        self._amount = float(value)


    @property
    def paid_on(self):
        return self._paid_on

    @paid_on.setter
    def paid_on(self,value):
        if not isinstance(value,date):
            raise TypeError ('input not date')
        self._paid_on = value


#_____________________________________________________________________________________________________
# methods (abstracted)
#_____________________________________________________________________________________________________

    @abstractmethod
    def process(self):
        '''process of payment for the order'''
        pass

    def get_amount(self) -> float:
        return self.amount




#_____________________________________________________________________________________________________
# payment classes (card or cash)
#_____________________________________________________________________________________________________


class CardPayment (Payment):
    def __init__(self,payment_id:str,amount:float,paid_on:date,card_last4:str):
        super().__init__(payment_id,amount,paid_on)
        self.card_last4 = card_last4

#------------------------------------
#setters and gitters for CardPayment
#------------------------------------


    @property
    def card_last4(self) :
        return self.__card_last4

    @card_last4.setter
    def card_last4(self,value):
        if not isinstance(value, str):
            raise TypeError("card last 4 has to be str")
        
        if len(value) != 4 or not value.isdigit():
            raise ValueError("card last 4 has to be exactly 4 digits")
        
        self.__card_last4 = value
        

    def process(self)->bool:
        return True

    def mask_card(self)->str:
        return f"****-****-****-{self.__card_last4}"



class CashPayment(Payment):
    def __init__(self,payment_id:str,amount:float,paid_on:date,tendered:float):
        super().__init__(payment_id,amount,paid_on)
        self.tendered = tendered

#------------------------------------
#setters and gitters for CashPayment
#------------------------------------


    @property
    def tendered(self) -> float:
        return self._tendered

    @tendered.setter
    def tendered(self, value):
        if not isinstance(value, (int,float)) or value < self.amount:
            raise ValueError("Tendered cash cannot be less than the amount due.")
        self._tendered = float(value)

    def process(self) -> bool:
        # Simulated cash processing logic
        return True

    def change(self) -> float:
        return self._tendered - self.amount