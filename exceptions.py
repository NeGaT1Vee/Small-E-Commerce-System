''' Validation rules Bisness Rules (BR) for the e-commerce system.
-------------------------------------------------------------------------
BR-01 Cannot purchase more than available stock. PDF

BR-02 Cannot checkout an empty cart. PDF

BR-03 Product price must be positive. PDF

BR-04 Order total is calculated automatically. PDF

BR-05 Stock is checked when adding to the cart and checked again at checkout. (derived)

BR-06 Checkout is all-or-nothing: if any step fails, stock and cart stay unchanged. (derived)

BR-07 Discount can never make the total negative (minimum 0.00). (derived)

BR-08 Order status changes only Pending -> Paid -> Shipped -> Delivered; Cancelled
from Pending or Paid only.
(derived)

BR-09 Cancelling a Pending or Paid order restores stock. (derived)

BR-10 OrderItem keeps the price paid even if the product price changes later. (derived)

BR-11 Payment amount must equal the order total. (derived),,,
'''

class ValidationError(Exception):
    pass

class TypeError(Exception):
    pass

class ValueError(Exception):
    pass
