from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from .value_objects import CurrencyCode, Money


@dataclass(frozen=True)
class SalesLine:
    sku: str
    units: int
    revenue: Money

    def __post_init__(self) -> None:
        if not self.sku.strip():
            raise ValueError("sku cannot be empty")
        if self.units <= 0:
            raise ValueError("units must be greater than zero")


@dataclass
class SalesAggregate:
    aggregate_id: str
    currency: CurrencyCode
    lines: list[SalesLine] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.aggregate_id.strip():
            raise ValueError("aggregate_id cannot be empty")
        self._validate_line_currencies()

    def add_line(self, line: SalesLine) -> None:
        if line.revenue.currency != self.currency:
            raise ValueError("line currency must match aggregate currency")
        self.lines.append(line)

    def total_units(self) -> int:
        return sum(line.units for line in self.lines)

    def total_revenue(self) -> Money:
        total = Decimal("0")
        for line in self.lines:
            total += line.revenue.amount
        return Money(amount=total, currency=self.currency)

    def _validate_line_currencies(self) -> None:
        for line in self.lines:
            if line.revenue.currency != self.currency:
                raise ValueError("line currency must match aggregate currency")
