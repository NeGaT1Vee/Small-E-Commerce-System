from models.payment import Payment
from datetime import date,time
class CardPayment(Payment):
    def __init__(self,card_last4:str,payment_id:str,amount:float,paid_on:date):
        super().__init__(payment_id,amount,paid_on)
        self.card_last4=card_last4

    @property
    def card_last4(self):
        return self.__card_last4
    @card_last4.setter
    def card_last4(self,value):
        if not isinstance(value,str):
            raise TypeError("value must be strig")
        if not value.strip():
            raise ValueError("value is empty")
        self.__card_last4=value
    #methods:-
    #1-process 
    def process(self) -> bool:
        if self.amount > 0 and len(self.card_last4) == 4:
            return True
        return False
       
    #2-mask_card:-
    def mask_card(self):
      return f"****-****-****-{self.card_last4}"