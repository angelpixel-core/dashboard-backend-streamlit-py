"""Ports for e-commerce data retrieval."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from dashboard.domain.ecommerce import (
    CourierCode,
    InventoryItem,
    Order,
    PaymentTransaction,
    Shipment,
)


class EcommerceDataReaderPort(Protocol):
    """Port interface for querying e-commerce operational data."""

    def list_orders(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        region: str | None = None,
    ) -> tuple[Order, ...]:
        """Fetch orders matching optional temporal and regional filters."""
        ...

    def list_payment_transactions(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        gateway: str | None = None,
    ) -> tuple[PaymentTransaction, ...]:
        """Fetch payment transactions with optional gateway and date filters."""
        ...

    def list_shipments(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        courier: CourierCode | None = None,
    ) -> tuple[Shipment, ...]:
        """Fetch shipments with optional courier and date filters."""
        ...

    def list_inventory_items(
        self,
        category: str | None = None,
        low_stock_only: bool = False,
    ) -> tuple[InventoryItem, ...]:
        """Fetch catalog inventory records with optional stock thresholds."""
        ...
