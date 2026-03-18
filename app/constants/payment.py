from enum import Enum

class Currency(Enum):
    USD = "USD"
    INR = "INR"

class PaymentMode(Enum):
    UPI = "upi"
    CARD = "card"
    