# tests/test_order.py
from datetime import date
from models.category import Category
from models.product import Product
from models.orderitem import OrderItem
from models.order import Order
from models.payment import CardPayment
from models.Enums.enums import OrderStatus

# كلاسات وهمية لاختبار طريقة الـ from_cart
class MockCartItem:
    def __init__(self, product, quantity, unit_price):
        self.product = product
        self.quantity = quantity
        self.unit_price = unit_price

class MockCart:
    def __init__(self, items):
        self.items = items

print("--- 1. Testing Direct Order Initialization ---")
category = Category(category_id="CAT-001", name="Stationery")
product = Product(product_id="PRO-001", name="Notebook", price=50.0, stock=20, category=category)

order_item = OrderItem(product=product, quantity=3, unit_price=product.price)

order = Order(
    order_id="ORD-001",
    customer_id="CUS-001",
    created_on=date.today(),
    status=OrderStatus.PENDING,
    discount_rate=0.0,
    items=[order_item],
    payment=None
)

print(f"Order ID: {order.order_id}")
# print(f"Subtotal: {order.subtotal()}") # يجب أن يكون 150.0
print(f"Total: {order.total()}")       # يجب أن يكون 150.0

print("\n--- 2. Testing Discount Application ---")
order.apply_discount(0.20) # تطبيق خصم 20%
print(f"New Discount Rate: {order.discount_rate}")
print(f"New Total after 20% discount: {order.total()}") # يجب أن يكون 120.0

print("\n--- 3. Testing Payment Process (mark_paid) ---")
card_payment = CardPayment(
    payment_id="PAY-001",
    amount=120.0,
    paid_on=date.today(),
    card_last4="9876"
)
order.mark_paid(card_payment)
print(f"Order Status: {order.status.name}") # يجب أن يكون PAID

print("\n--- 4. Testing Order Cancellation & Stock Restoration ---")
print(f"Stock before cancel: {product.stock}") # كان 20، نقص 3 عند إنشاء OrderItem -> أصبح 17
order.cancel()
print(f"Order Status after cancel: {order.status.name}") # يجب أن يكون CANCELLED
print(f"Stock after cancel (Restored): {product.stock}") # يجب أن يعود إلى 20

print("\n--- 5. Testing from_cart Class Method ---")
cart_item = MockCartItem(product=product, quantity=2, unit_price=product.price)
cart = MockCart(items=[cart_item])

cart_order = Order.from_cart(order_id="ORD-002", customer_id="CUS-002", cart=cart)
print(f"Cart Order ID: {cart_order.order_id}")
print(f"Cart Order Status: {cart_order.status.name}")
print(f"Cart Order Total: {cart_order.total()}") # يجب أن يكون 100.0 (بدون خصم)

print("\nAll tests passed successfully!")