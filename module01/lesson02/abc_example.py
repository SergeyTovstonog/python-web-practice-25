from abc import ABC, abstractmethod
from enum import Enum


class PaymentProviders(Enum):

    STRIPE = "stripe"
    PAYPAL = "paypal"


class PaymentProvider(ABC):

    @abstractmethod
    def make_payment(self):
       pass

    @abstractmethod
    def validate_payment(self):
        pass

    @abstractmethod
    def refund_payment(self):
        pass


class StripePaymentProvider(PaymentProvider):

    def make_payment(self):
        print("Making payment with Stripe")

    def validate_payment(self):
        print("Validating payment with Stripe")

    def refund_payment(self):
        print("Refunding payment with Stripe")


class PayPalPaymentProvider(PaymentProvider):
    def make_payment(self):
        print("Making payment with PayPal")

    def validate_payment(self):
        print("Verifying payment with PayPal")

class NewPayPalPaymentProvider(PayPalPaymentProvider):
    pass

def choose_payment_method(payment_method: PaymentProviders) -> PaymentProvider:

    if payment_method == PaymentProviders.STRIPE:
        return StripePaymentProvider()
    elif payment_method == PaymentProviders.PAYPAL:
        return NewPayPalPaymentProvider()
    else:
        raise ValueError("Invalid payment method")




if __name__ == "__main__":
    payment_provider = PayPalPaymentProvider()

    payment_provider.make_payment()
    # This will raise an error
    payment_provider.validate_payment()

    choose_payment_method(PaymentProviders.STRIPE)