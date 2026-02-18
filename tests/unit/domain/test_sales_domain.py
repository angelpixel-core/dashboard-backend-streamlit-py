from decimal import Decimal

import pytest

from dashboard.domain.sales import (
    CurrencyCode,
    Money,
    SalesAggregate,
    SalesLine,
    build_sales_aggregate,
)


def test_currency_code_normalizes_input() -> None:
    code = CurrencyCode(" usd ")
    assert code.code == "USD"


def test_currency_code_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="3-letter"):
        CurrencyCode("us")


def test_money_addition_requires_same_currency() -> None:
    usd = CurrencyCode("USD")
    eur = CurrencyCode("EUR")
    left = Money(amount=Decimal("10"), currency=usd)
    right = Money(amount=Decimal("5"), currency=eur)

    with pytest.raises(ValueError, match="different currencies"):
        _ = left + right


def test_sales_line_requires_positive_units() -> None:
    usd = CurrencyCode("USD")
    with pytest.raises(ValueError, match="greater than zero"):
        SalesLine(
            sku="SKU-001",
            units=0,
            revenue=Money(amount=Decimal("10"), currency=usd),
        )


def test_sales_aggregate_computes_totals() -> None:
    usd = CurrencyCode("USD")
    line_a = SalesLine(
        sku="SKU-001",
        units=2,
        revenue=Money(amount=Decimal("10"), currency=usd),
    )
    line_b = SalesLine(
        sku="SKU-002",
        units=3,
        revenue=Money(amount=Decimal("15"), currency=usd),
    )
    aggregate = build_sales_aggregate(
        aggregate_id="sales-overview",
        currency=usd,
        lines=[line_a, line_b],
    )

    assert aggregate.total_units() == 5
    assert aggregate.total_revenue() == Money(
        amount=Decimal("25"),
        currency=usd,
    )


def test_sales_aggregate_rejects_mixed_currency_line() -> None:
    usd = CurrencyCode("USD")
    eur = CurrencyCode("EUR")
    aggregate = SalesAggregate(aggregate_id="sales-overview", currency=usd)

    with pytest.raises(ValueError, match="must match aggregate currency"):
        aggregate.add_line(
            SalesLine(
                sku="SKU-003",
                units=1,
                revenue=Money(amount=Decimal("7"), currency=eur),
            ),
        )
