"""Value objects for the e-commerce domain."""

from __future__ import annotations

from enum import StrEnum


class OrderStatus(StrEnum):
    """Lifecycle status of an e-commerce order."""

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"


class PaymentStatus(StrEnum):
    """Transaction status for payment processing."""

    PENDING = "PENDING"
    CAPTURED = "CAPTURED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    CHARGEBACK = "CHARGEBACK"


class PaymentMethod(StrEnum):
    """Payment methods supported by the checkout."""

    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    BANK_TRANSFER = "BANK_TRANSFER"
    DIGITAL_WALLET = "DIGITAL_WALLET"
    CASH_ON_DELIVERY = "CASH_ON_DELIVERY"


class PaymentFailureReason(StrEnum):
    """Reason code for failed payment transactions."""

    NONE = "NONE"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    SUSPECTED_FRAUD = "SUSPECTED_FRAUD"
    EXPIRED_CARD = "EXPIRED_CARD"
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"


class ShipmentStatus(StrEnum):
    """Status of logistics and fulfillment delivery."""

    PENDING_DISPATCH = "PENDING_DISPATCH"
    DISPATCHED = "DISPATCHED"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    FAILED_ATTEMPT = "FAILED_ATTEMPT"
    RETURNED_TO_ORIGIN = "RETURNED_TO_ORIGIN"


class CourierCode(StrEnum):
    """Logistics couriers and fulfillment partners."""

    DHL = "DHL"
    FEDEX = "FEDEX"
    UPS = "UPS"
    LOCAL_EXPRESS = "LOCAL_EXPRESS"
