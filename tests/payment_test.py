from models.payment import CardPayment,CashPayment
from models.__init__ import date

print("--- Testing CardPayment ---")
card = CardPayment(
    payment_id="PAY-001",
    amount=150.0,
    paid_on=date.today(),
    card_last4="4242"
)

print("Payment ID:", card.payment_id)
print("Amount Due:", card.get_amount())
print("Masked Card:", card.mask_card())
print("Process Status:", card.process())

print("\n--- Testing CashPayment ---")
cash = CashPayment(
    payment_id="PAY-002",
    amount=75.50,
    paid_on=date.today(),
    tendered=100.0
)

print("Change to return:", cash.change())