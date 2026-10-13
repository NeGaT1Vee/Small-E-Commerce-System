from enum import Enum


class OrderStatus(Enum):

    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
