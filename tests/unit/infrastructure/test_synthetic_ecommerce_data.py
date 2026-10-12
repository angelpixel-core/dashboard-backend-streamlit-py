"""Unit tests for synthetic e-commerce data generator and in-memory reader."""

from decimal import Decimal

from dashboard.domain.ecommerce import (
    CourierCode,
    OrderStatus,
    PaymentStatus,
)
from dashboard.infrastructure.persistence import (
    SyntheticEcommerceDataGenerator,
    build_synthetic_ecommerce_reader,
)


def test_generator_determinism() -> None:
    gen1 = SyntheticEcommerceDataGenerator(seed=123)
    orders1, payments1, shipments1, inventory1 = gen1.generate(num_orders=50)

    gen2 = SyntheticEcommerceDataGenerator(seed=123)
    orders2, payments2, shipments2, inventory2 = gen2.generate(num_orders=50)

    assert len(orders1) == 50
    assert len(orders2) == 50
    assert orders1[0].order_id == orders2[0].order_id
    assert orders1[0].total_amount() == orders2[0].total_amount()
    assert len(payments1) == len(payments2)
    assert len(shipments1) == len(shipments2)
    assert len(inventory1) == len(inventory2)


def test_generator_structure_and_relations() -> None:
    generator = SyntheticEcommerceDataGenerator(seed=42)
    orders, payments, shipments, inventory = generator.generate(num_orders=100)

    assert len(orders) == 100
    assert len(payments) == 100
    assert len(inventory) == 16

    # Verify inventory has low stock items
    low_stock = [item for item in inventory if item.is_low_stock()]
    assert len(low_stock) > 0

    # Verify every order has a corresponding payment
    order_ids = {o.order_id for o in orders}
    for pay in payments:
        assert pay.order_id in order_ids
        assert pay.amount.amount > Decimal("0")

    # Verify cancelled orders have failed payments
    cancelled = [o for o in orders if o.status == OrderStatus.CANCELLED]
    assert len(cancelled) > 0
    for cancel_order in cancelled:
        match_pay = next(
            p for p in payments if p.order_id == cancel_order.order_id
        )
        assert match_pay.status == PaymentStatus.FAILED

    # Verify shipments link to valid orders
    for ship in shipments:
        assert ship.order_id in order_ids


def test_in_memory_reader_filters() -> None:
    reader = build_synthetic_ecommerce_reader(seed=42, num_orders=200)

    # Test order filtering by region
    north_orders = reader.list_orders(region="North")
    assert all(o.region == "North" for o in north_orders)
    assert len(north_orders) > 0

    # Test payment filtering by gateway
    stripe_payments = reader.list_payment_transactions(gateway="Stripe")
    assert all(p.gateway == "Stripe" for p in stripe_payments)
    assert len(stripe_payments) > 0

    # Test shipment filtering by courier
    dhl_shipments = reader.list_shipments(courier=CourierCode.DHL)
    assert all(s.courier == CourierCode.DHL for s in dhl_shipments)

    # Test inventory filtering
    elec_items = reader.list_inventory_items(category="Electronics")
    assert all(i.category == "Electronics" for i in elec_items)
    assert len(elec_items) == 4

    low_stock_items = reader.list_inventory_items(low_stock_only=True)
    assert all(i.is_low_stock() for i in low_stock_items)
    assert len(low_stock_items) > 0


def test_in_memory_reader_date_filters() -> None:
    reader = build_synthetic_ecommerce_reader(seed=42, num_orders=100)
    all_orders = reader.list_orders()
    assert len(all_orders) == 100

    min_date = all_orders[20].created_at
    max_date = all_orders[60].created_at

    ranged_orders = reader.list_orders(start_date=min_date, end_date=max_date)
    assert all(min_date <= o.created_at <= max_date for o in ranged_orders)
    assert len(ranged_orders) <= 100
