"""Entities and aggregates for the e-commerce domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from dashboard.domain.sales.value_objects import Money

from .value_objects import (
    CourierCode,
    OrderStatus,
    PaymentFailureReason,
    PaymentMethod,
    PaymentStatus,
    ShipmentStatus,
)


@dataclass(frozen=True)
class OrderItem:
    """Individual item line within an order."""

    sku: str
    name: str
    category: str
    quantity: int
    unit_price: Money

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("sku cannot be empty")
        if not self.name.strip():
            raise ValueError("name cannot be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than zero")

    def subtotal(self) -> Money:
        """Calculate total amount for this line item."""
        return Money(
            amount=self.unit_price.amount * Decimal(self.quantity),
            currency=self.unit_price.currency,
        )


@dataclass(frozen=True)
class Order:
    """Customer purchase order aggregate."""

    order_id: str
    customer_id: str
    created_at: datetime
    items: tuple[OrderItem, ...]
    status: OrderStatus
    region: str
    shipping_address: str

    def __post_init__(self) -> None:
        if not self.order_id.strip():
            raise ValueError("order_id cannot be empty")
        if not self.customer_id.strip():
            raise ValueError("customer_id cannot be empty")
        if not self.items:
            raise ValueError("order must contain at least one item")
        self._validate_currencies()

    def _validate_currencies(self) -> None:
        first_currency = self.items[0].unit_price.currency
        for item in self.items:
            if item.unit_price.currency != first_currency:
                raise ValueError("all items in order must have same currency")

    def total_amount(self) -> Money:
        """Sum total monetary amount across all order lines."""
        currency = self.items[0].unit_price.currency
        total = Decimal("0")
        for item in self.items:
            total += item.subtotal().amount
        return Money(amount=total, currency=currency)

    def total_items(self) -> int:
        """Sum unit quantity of all lines."""
        return sum(item.quantity for item in self.items)


@dataclass(frozen=True)
class PaymentTransaction:
    """Transaction attempt against payment gateway."""

    transaction_id: str
    order_id: str
    timestamp: datetime
    amount: Money
    status: PaymentStatus
    payment_method: PaymentMethod
    gateway: str
    failure_reason: PaymentFailureReason = PaymentFailureReason.NONE

    def __post_init__(self) -> None:
        if not self.transaction_id.strip():
            raise ValueError("transaction_id cannot be empty")
        if not self.order_id.strip():
            raise ValueError("order_id cannot be empty")
        if not self.gateway.strip():
            raise ValueError("gateway cannot be empty")


@dataclass(frozen=True)
class Shipment:
    """Fulfillment dispatch and carrier delivery record."""

    shipment_id: str
    order_id: str
    courier: CourierCode
    status: ShipmentStatus
    dispatched_at: datetime | None
    delivered_at: datetime | None
    estimated_delivery_at: datetime
    shipping_fee: Money

    def __post_init__(self) -> None:
        if not self.shipment_id.strip():
            raise ValueError("shipment_id cannot be empty")
        if not self.order_id.strip():
            raise ValueError("order_id cannot be empty")

    def is_delayed(self, reference_time: datetime) -> bool:
        """Check if delivery exceeded estimated delivery target."""
        if self.delivered_at is not None:
            return self.delivered_at > self.estimated_delivery_at
        return reference_time > self.estimated_delivery_at

    def lead_time_hours(self) -> float | None:
        """Compute transit duration in hours from dispatch to delivery."""
        if self.dispatched_at is None or self.delivered_at is None:
            return None
        diff = self.delivered_at - self.dispatched_at
        return diff.total_seconds() / 3600.0


@dataclass(frozen=True)
class InventoryItem:
    """Catalog inventory tracking record for a SKU."""

    sku: str
    name: str
    category: str
    stock_quantity: int
    safety_stock_threshold: int
    unit_cost: Money

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("sku cannot be empty")
        if self.stock_quantity < 0:
            raise ValueError("stock_quantity cannot be negative")
        if self.safety_stock_threshold < 0:
            raise ValueError("safety_stock_threshold cannot be negative")

    def is_low_stock(self) -> bool:
        """Check if stock level is below safety threshold."""
        return self.stock_quantity <= self.safety_stock_threshold

    def is_out_of_stock(self) -> bool:
        """Check if product is completely sold out."""
        return self.stock_quantity == 0
