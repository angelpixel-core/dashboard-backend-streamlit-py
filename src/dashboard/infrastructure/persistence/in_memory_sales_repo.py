from dataclasses import dataclass
from decimal import Decimal

from dashboard.application.ports import SalesAggregateReader
from dashboard.domain.sales import (
    CurrencyCode,
    Money,
    SalesAggregate,
    SalesLine,
)


@dataclass(frozen=True)
class InMemorySalesRecord:
    sku: str
    units: int
    revenue: Decimal


@dataclass
class InMemorySalesAggregateReader(SalesAggregateReader):
    aggregate_id: str
    currency: str
    records: tuple[InMemorySalesRecord, ...]

    def get_sales_aggregate(self, aggregate_id: str) -> SalesAggregate:
        if aggregate_id != self.aggregate_id:
            raise KeyError(f"aggregate not found: {aggregate_id}")

        currency = CurrencyCode(self.currency)
        lines = [
            SalesLine(
                sku=record.sku,
                units=record.units,
                revenue=Money(amount=record.revenue, currency=currency),
            )
            for record in self.records
        ]
        return SalesAggregate(
            aggregate_id=aggregate_id,
            currency=currency,
            lines=lines,
        )
