"""Synthetic e-commerce dataset generator and in-memory reader adapter."""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from decimal import Decimal

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

CURRENCY_USD = CurrencyCode("USD")

CATALOG_SPECS: tuple[tuple[str, str, str, Decimal, Decimal], ...] = (
    (
        "SKU-ELEC-01",
        "Pro Laptop 15",
        "Electronics",
        Decimal("1200"),
        Decimal("850"),
    ),
    (
        "SKU-ELEC-02",
        "Wireless Headphones",
        "Electronics",
        Decimal("150"),
        Decimal("80"),
    ),
    (
        "SKU-ELEC-03",
        "Mechanical Keyboard",
        "Electronics",
        Decimal("95"),
        Decimal("50"),
    ),
    (
        "SKU-ELEC-04",
        "Ultra HD Monitor 27",
        "Electronics",
        Decimal("340"),
        Decimal("220"),
    ),
    (
        "SKU-HOME-01",
        "Ergonomic Desk Chair",
        "Home & Living",
        Decimal("280"),
        Decimal("170"),
    ),
    (
        "SKU-HOME-02",
        "Smart LED Desk Lamp",
        "Home & Living",
        Decimal("60"),
        Decimal("30"),
    ),
    (
        "SKU-HOME-03",
        "Espresso Machine Pro",
        "Home & Living",
        Decimal("210"),
        Decimal("130"),
    ),
    (
        "SKU-HOME-04",
        "HEPA Air Purifier",
        "Home & Living",
        Decimal("180"),
        Decimal("110"),
    ),
    (
        "SKU-APPA-01",
        "Performance Hoodie",
        "Apparel",
        Decimal("75"),
        Decimal("35"),
    ),
    (
        "SKU-APPA-02",
        "Road Running Shoes",
        "Apparel",
        Decimal("120"),
        Decimal("65"),
    ),
    (
        "SKU-APPA-03",
        "Waterproof Commuter Bag",
        "Apparel",
        Decimal("90"),
        Decimal("45"),
    ),
    (
        "SKU-APPA-04",
        "Windbreaker Thermal Jacket",
        "Apparel",
        Decimal("140"),
        Decimal("75"),
    ),
    (
        "SKU-BEAU-01",
        "Hyaluronic Acid Serum",
        "Beauty & Care",
        Decimal("35"),
        Decimal("12"),
    ),
    (
        "SKU-BEAU-02",
        "Hydrating Facial Cleanser",
        "Beauty & Care",
        Decimal("25"),
        Decimal("9"),
    ),
    (
        "SKU-BEAU-03",
        "Mineral Sunscreen SPF50",
        "Beauty & Care",
        Decimal("30"),
        Decimal("11"),
    ),
    (
        "SKU-BEAU-04",
        "Revitalizing Night Cream",
        "Beauty & Care",
        Decimal("45"),
        Decimal("18"),
    ),
)

REGIONS: tuple[str, ...] = ("North", "South", "East", "West", "Central")
GATEWAYS: tuple[str, ...] = ("Stripe", "MercadoPago", "PayPal", "Adyen")
COURIERS: tuple[CourierCode, ...] = (
    CourierCode.DHL,
    CourierCode.FEDEX,
    CourierCode.UPS,
    CourierCode.LOCAL_EXPRESS,
)


class SyntheticEcommerceDataGenerator:
    """Generates deterministic, statistically realistic e-commerce datasets."""

    def __init__(
        self, seed: int = 42, base_date: datetime | None = None
    ) -> None:
        """Initialize generator with random seed and reference timestamp."""
        self._rng = random.Random(seed)
        self._base_date = base_date or datetime(2026, 10, 1, 12, 0, 0)

    def generate(
        self,
        num_orders: int = 500,
        days_span: int = 60,
    ) -> tuple[
        tuple[Order, ...],
        tuple[PaymentTransaction, ...],
        tuple[Shipment, ...],
        tuple[InventoryItem, ...],
    ]:
        """Generate orders, payments, shipments, and inventory items."""
        inventory = self._build_inventory()
        orders: list[Order] = []
        payments: list[PaymentTransaction] = []
        shipments: list[Shipment] = []

        for i in range(1, num_orders + 1):
            order, payment, shipment = self._generate_single_cycle(
                index=i,
                days_span=days_span,
            )
            orders.append(order)
            payments.append(payment)
            if shipment is not None:
                shipments.append(shipment)

        orders.sort(key=lambda o: o.created_at)
        payments.sort(key=lambda p: p.timestamp)
        shipments.sort(key=lambda s: s.estimated_delivery_at)

        return (
            tuple(orders),
            tuple(payments),
            tuple(shipments),
            inventory,
        )

    def _build_inventory(self) -> tuple[InventoryItem, ...]:
        items: list[InventoryItem] = []
        for i, (sku, name, cat, _, cost) in enumerate(CATALOG_SPECS):
            # Introduce controlled low stock and stockout conditions
            if i == 0:
                stock = 0
                threshold = 5
            elif i in (1, 5, 9):
                stock = 4
                threshold = 10
            else:
                stock = self._rng.randint(25, 250)
                threshold = self._rng.randint(10, 20)

            items.append(
                InventoryItem(
                    sku=sku,
                    name=name,
                    category=cat,
                    stock_quantity=stock,
                    safety_stock_threshold=threshold,
                    unit_cost=Money(amount=cost, currency=CURRENCY_USD),
                )
            )
        return tuple(items)

    def _generate_single_cycle(
        self,
        index: int,
        days_span: int,
    ) -> tuple[Order, PaymentTransaction, Shipment | None]:
        offset_seconds = self._rng.randint(0, days_span * 86400)
        order_date = self._base_date - timedelta(seconds=offset_seconds)
        order_id = f"ORD-{index:05d}"
        customer_id = f"CUST-{self._rng.randint(100, 999)}"
        region = self._rng.choice(REGIONS)

        item_count = self._rng.choices([1, 2, 3, 4], weights=[45, 35, 15, 5])[0]
        selected_specs = self._rng.sample(CATALOG_SPECS, item_count)
        order_items = tuple(
            OrderItem(
                sku=spec[0],
                name=spec[1],
                category=spec[2],
                quantity=self._rng.randint(1, 3),
                unit_price=Money(amount=spec[3], currency=CURRENCY_USD),
            )
            for spec in selected_specs
        )

        # Payment simulation: ~88% approval rate
        is_payment_success = self._rng.random() < 0.88
        payment_method = self._rng.choice(list(PaymentMethod))
        gateway = self._rng.choice(GATEWAYS)
        payment_time = order_date + timedelta(
            seconds=self._rng.randint(30, 300)
        )

        if is_payment_success:
            pay_status = PaymentStatus.CAPTURED
            fail_reason = PaymentFailureReason.NONE
        else:
            pay_status = PaymentStatus.FAILED
            fail_reason = self._rng.choice(
                [
                    PaymentFailureReason.INSUFFICIENT_FUNDS,
                    PaymentFailureReason.SUSPECTED_FRAUD,
                    PaymentFailureReason.EXPIRED_CARD,
                    PaymentFailureReason.GATEWAY_TIMEOUT,
                ]
            )

        # Compute total
        total_amount = Decimal("0")
        for item in order_items:
            total_amount += item.subtotal().amount

        payment = PaymentTransaction(
            transaction_id=f"TXN-{index:05d}",
            order_id=order_id,
            timestamp=payment_time,
            amount=Money(amount=total_amount, currency=CURRENCY_USD),
            status=pay_status,
            payment_method=payment_method,
            gateway=gateway,
            failure_reason=fail_reason,
        )

        if not is_payment_success:
            order = Order(
                order_id=order_id,
                customer_id=customer_id,
                created_at=order_date,
                items=order_items,
                status=OrderStatus.CANCELLED,
                region=region,
                shipping_address=f"Street {index}, {region} Zone",
            )
            return order, payment, None

        # Successful payment -> determine order & shipment lifecycle
        age_hours = (self._base_date - order_date).total_seconds() / 3600.0
        courier = self._rng.choice(COURIERS)
        shipment_fee = Money(
            amount=Decimal(self._rng.randint(8, 25)),
            currency=CURRENCY_USD,
        )

        if age_hours < 12:
            order_status = OrderStatus.CONFIRMED
            shipment = None
        elif age_hours < 24:
            order_status = OrderStatus.PROCESSING
            shipment = None
        elif age_hours < 72:
            order_status = OrderStatus.SHIPPED
            dispatched = order_date + timedelta(hours=14)
            estimated = dispatched + timedelta(days=2)
            shipment = Shipment(
                shipment_id=f"SHIP-{index:05d}",
                order_id=order_id,
                courier=courier,
                status=ShipmentStatus.IN_TRANSIT,
                dispatched_at=dispatched,
                delivered_at=None,
                estimated_delivery_at=estimated,
                shipping_fee=shipment_fee,
            )
        else:
            order_status = OrderStatus.DELIVERED
            dispatched = order_date + timedelta(hours=12)
            estimated = dispatched + timedelta(days=2)
            # 90% on-time, 10% delayed delivery
            is_delayed = self._rng.random() < 0.10
            delay_hours = 60 if is_delayed else 36
            delivered = dispatched + timedelta(hours=delay_hours)
            shipment = Shipment(
                shipment_id=f"SHIP-{index:05d}",
                order_id=order_id,
                courier=courier,
                status=ShipmentStatus.DELIVERED,
                dispatched_at=dispatched,
                delivered_at=delivered,
                estimated_delivery_at=estimated,
                shipping_fee=shipment_fee,
            )

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            created_at=order_date,
            items=order_items,
            status=order_status,
            region=region,
            shipping_address=f"Street {index}, {region} Zone",
        )
        return order, payment, shipment


class InMemoryEcommerceDataReader:
    """In-memory adapter implementing EcommerceDataReaderPort."""

    def __init__(
        self,
        orders: tuple[Order, ...] = (),
        payments: tuple[PaymentTransaction, ...] = (),
        shipments: tuple[Shipment, ...] = (),
        inventory: tuple[InventoryItem, ...] = (),
    ) -> None:
        """Initialize in-memory data store with domain tuples."""
        self._orders = orders
        self._payments = payments
        self._shipments = shipments
        self._inventory = inventory

    def list_orders(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        region: str | None = None,
    ) -> tuple[Order, ...]:
        """Fetch orders with date and regional filtering."""
        filtered = self._orders
        if start_date is not None:
            filtered = tuple(o for o in filtered if o.created_at >= start_date)
        if end_date is not None:
            filtered = tuple(o for o in filtered if o.created_at <= end_date)
        if region is not None:
            filtered = tuple(o for o in filtered if o.region == region)
        return filtered

    def list_payment_transactions(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        gateway: str | None = None,
    ) -> tuple[PaymentTransaction, ...]:
        """Fetch payment transactions with date and gateway filtering."""
        filtered = self._payments
        if start_date is not None:
            filtered = tuple(p for p in filtered if p.timestamp >= start_date)
        if end_date is not None:
            filtered = tuple(p for p in filtered if p.timestamp <= end_date)
        if gateway is not None:
            filtered = tuple(p for p in filtered if p.gateway == gateway)
        return filtered

    def list_shipments(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        courier: CourierCode | None = None,
    ) -> tuple[Shipment, ...]:
        """Fetch shipments with date and courier filtering."""
        filtered = self._shipments
        if start_date is not None:
            filtered = tuple(
                s
                for s in filtered
                if s.dispatched_at is not None and s.dispatched_at >= start_date
            )
        if end_date is not None:
            filtered = tuple(
                s
                for s in filtered
                if s.dispatched_at is not None and s.dispatched_at <= end_date
            )
        if courier is not None:
            filtered = tuple(s for s in filtered if s.courier == courier)
        return filtered

    def list_inventory_items(
        self,
        category: str | None = None,
        low_stock_only: bool = False,
    ) -> tuple[InventoryItem, ...]:
        """Fetch inventory items with category and low stock filtering."""
        filtered = self._inventory
        if category is not None:
            filtered = tuple(i for i in filtered if i.category == category)
        if low_stock_only:
            filtered = tuple(i for i in filtered if i.is_low_stock())
        return filtered


def build_synthetic_ecommerce_reader(
    seed: int = 42,
    num_orders: int = 500,
) -> InMemoryEcommerceDataReader:
    """Helper factory to instantiate ready-to-query dataset reader."""
    generator = SyntheticEcommerceDataGenerator(seed=seed)
    orders, payments, shipments, inventory = generator.generate(
        num_orders=num_orders,
    )
    return InMemoryEcommerceDataReader(
        orders=orders,
        payments=payments,
        shipments=shipments,
        inventory=inventory,
    )
