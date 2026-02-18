from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CurrencyCode:
    code: str

    def __post_init__(self) -> None:
        normalized = self.code.strip().upper()
        if len(normalized) != 3 or not normalized.isalpha():
            raise ValueError("currency code must be a 3-letter ISO-like value")
        object.__setattr__(self, "code", normalized)


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: CurrencyCode

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise ValueError("money amount cannot be negative")

    def __add__(self, other: Money) -> Money:
        self._assert_same_currency(other)
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def _assert_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise ValueError("cannot operate with different currencies")
