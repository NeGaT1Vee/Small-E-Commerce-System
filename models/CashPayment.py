from models.payment import Payment
from datetime import date
class CashPayment(Payment):
    def __init__(self,tendered:float,payment_id:str,amount:float,paid_on:date):
        super().__init__(payment_id,amount,paid_on)
        self.tendered=tendered

    @property
    def tendered(self):
        return self.__tendered
    @tendered.setter
    def tendered(self,new_tendered):
        if not isinstance(new_tendered,(int,float)):
            raise TypeError("invalid tendered")
        if not str(new_tendered).strip() or new_tendered<=0:
            raise ValueError("enter a valid tendered")
        self.__tendered=new_tendered
    #methods:-
    #1-process
    def process(self):
        if self.__tendered>=self.amount:
            return True
        else:
            return False
    #2-change
    def change(self):
        change=self.__tendered-self.amount
        return float(change)