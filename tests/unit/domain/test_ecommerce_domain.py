"""Unit tests for the e-commerce domain models and aggregates."""

from datetime import datetime
from decimal import Decimal

import pytest

from dashboard.domain.ecommerce import (
    CourierCode,
    InventoryItem,
    Order,
    OrderItem,
    OrderStatus,
    PaymentFailureReason,
    PaymentMethod,
    PaymentStatus,
    PaymentTransaction,
    Shipment,
    ShipmentStatus,
)
from dashboard.domain.sales.value_objects import CurrencyCode, Money

USD = CurrencyCode("USD")
EUR = CurrencyCode("EUR")


def test_order_item_calculates_subtotal() -> None:
    item = OrderItem(
        sku="SKU-001",
        name="Laptop Stand",
        category="Office",
        quantity=3,
        unit_price=Money(amount=Decimal("45"), currency=USD),
    )
    assert item.subtotal() == Money(amount=Decimal("135"), currency=USD)


def test_order_item_validations() -> None:
    with pytest.raises(ValueError, match="sku cannot be empty"):
        OrderItem(
            sku="  ",
            name="Valid Name",
            category="Office",
            quantity=1,
            unit_price=Money(amount=Decimal("10"), currency=USD),
        )

    with pytest.raises(ValueError, match="name cannot be empty"):
        OrderItem(
            sku="SKU-001",
            name=" ",
            category="Office",
            quantity=1,
            unit_price=Money(amount=Decimal("10"), currency=USD),
        )

    with pytest.raises(ValueError, match="quantity must be greater than zero"):
        OrderItem(
            sku="SKU-001",
            name="Valid",
            category="Office",
            quantity=0,
            unit_price=Money(amount=Decimal("10"), currency=USD),
        )


def test_order_computes_totals() -> None:
    item1 = OrderItem(
        sku="SKU-001",
        name="Item 1",
        category="Cat 1",
        quantity=2,
        unit_price=Money(amount=Decimal("50"), currency=USD),
    )
    item2 = OrderItem(
        sku="SKU-002",
        name="Item 2",
        category="Cat 2",
        quantity=1,
        unit_price=Money(amount=Decimal("30"), currency=USD),
    )
    order = Order(
        order_id="ORD-001",
        customer_id="CUST-100",
        created_at=datetime(2026, 10, 1, 10, 0),
        items=(item1, item2),
        status=OrderStatus.CONFIRMED,
        region="North",
        shipping_address="123 Main St",
    )

    assert order.total_items() == 3
    assert order.total_amount() == Money(amount=Decimal("130"), currency=USD)


def test_order_rejects_empty_items() -> None:
    with pytest.raises(ValueError, match="at least one item"):
        Order(
            order_id="ORD-001",
            customer_id="CUST-100",
            created_at=datetime(2026, 10, 1, 10, 0),
            items=(),
            status=OrderStatus.PENDING,
            region="North",
            shipping_address="123 Main St",
        )


def test_order_rejects_mixed_currencies() -> None:
    item_usd = OrderItem(
        sku="SKU-001",
        name="Item 1",
        category="Cat",
        quantity=1,
        unit_price=Money(amount=Decimal("50"), currency=USD),
    )
    item_eur = OrderItem(
        sku="SKU-002",
        name="Item 2",
        category="Cat",
        quantity=1,
        unit_price=Money(amount=Decimal("50"), currency=EUR),
    )
    with pytest.raises(ValueError, match="same currency"):
        Order(
            order_id="ORD-001",
            customer_id="CUST-100",
            created_at=datetime(2026, 10, 1, 10, 0),
            items=(item_usd, item_eur),
            status=OrderStatus.PENDING,
            region="North",
            shipping_address="123 Main St",
        )


def test_payment_transaction_validations() -> None:
    tx = PaymentTransaction(
        transaction_id="TXN-001",
        order_id="ORD-001",
        timestamp=datetime(2026, 10, 1, 10, 5),
        amount=Money(amount=Decimal("100"), currency=USD),
        status=PaymentStatus.CAPTURED,
        payment_method=PaymentMethod.CREDIT_CARD,
        gateway="Stripe",
    )
    assert tx.failure_reason == PaymentFailureReason.NONE

    with pytest.raises(ValueError, match="transaction_id cannot be empty"):
        PaymentTransaction(
            transaction_id="",
            order_id="ORD-001",
            timestamp=datetime(2026, 10, 1, 10, 5),
            amount=Money(amount=Decimal("100"), currency=USD),
            status=PaymentStatus.CAPTURED,
            payment_method=PaymentMethod.CREDIT_CARD,
            gateway="Stripe",
        )


def test_shipment_delay_and_lead_time() -> None:
    dispatched = datetime(2026, 10, 1, 8, 0)
    estimated = datetime(2026, 10, 3, 18, 0)
    delivered = datetime(2026, 10, 4, 10, 0)

    shipment = Shipment(
        shipment_id="SHIP-001",
        order_id="ORD-001",
        courier=CourierCode.DHL,
        status=ShipmentStatus.DELIVERED,
        dispatched_at=dispatched,
        delivered_at=delivered,
        estimated_delivery_at=estimated,
        shipping_fee=Money(amount=Decimal("15"), currency=USD),
    )

    assert shipment.is_delayed(datetime(2026, 10, 5, 0, 0)) is True
    # Lead time in hours: from Oct 1 08:00 to Oct 4 10:00 = 74 hours
    assert shipment.lead_time_hours() == 74.0


def test_inventory_item_low_stock_and_out_of_stock() -> None:
    item_normal = InventoryItem(
        sku="SKU-001",
        name="Keyboard",
        category="Electronics",
        stock_quantity=50,
        safety_stock_threshold=10,
        unit_cost=Money(amount=Decimal("20"), currency=USD),
    )
    assert item_normal.is_low_stock() is False
    assert item_normal.is_out_of_stock() is False

    item_low = InventoryItem(
        sku="SKU-002",
        name="Mouse",
        category="Electronics",
        stock_quantity=8,
        safety_stock_threshold=10,
        unit_cost=Money(amount=Decimal("15"), currency=USD),
    )
    assert item_low.is_low_stock() is True
    assert item_low.is_out_of_stock() is False

    item_zero = InventoryItem(
        sku="SKU-003",
        name="Monitor",
        category="Electronics",
        stock_quantity=0,
        safety_stock_threshold=5,
        unit_cost=Money(amount=Decimal("100"), currency=USD),
    )
    assert item_zero.is_low_stock() is True
    assert item_zero.is_out_of_stock() is True
