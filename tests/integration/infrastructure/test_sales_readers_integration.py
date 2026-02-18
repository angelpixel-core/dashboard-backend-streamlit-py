from decimal import Decimal

import pytest

from dashboard.infrastructure.persistence import (
    InMemorySalesAggregateReader,
    InMemorySalesRecord,
    SqlAlchemySalesAggregateReader,
)


def test_in_memory_reader_builds_sales_aggregate() -> None:
    reader = InMemorySalesAggregateReader(
        aggregate_id="sales-overview",
        currency="USD",
        records=(
            InMemorySalesRecord("SKU-001", 2, Decimal("10")),
            InMemorySalesRecord("SKU-002", 3, Decimal("15")),
        ),
    )

    aggregate = reader.get_sales_aggregate("sales-overview")

    assert aggregate.aggregate_id == "sales-overview"
    assert aggregate.currency.code == "USD"
    assert aggregate.total_units() == 5
    assert aggregate.total_revenue().amount == Decimal("25")


def test_in_memory_reader_raises_for_unknown_aggregate() -> None:
    reader = InMemorySalesAggregateReader(
        aggregate_id="known-id",
        currency="USD",
        records=(),
    )

    with pytest.raises(KeyError, match="aggregate not found"):
        reader.get_sales_aggregate("unknown-id")


class FakeResult:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self._rows = rows

    def mappings(self) -> list[dict[str, object]]:
        return self._rows


class FakeSession:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows
        self.statement = ""
        self.params: dict[str, object] = {}

    def execute(
        self,
        statement: str,
        params: dict[str, object],
    ) -> FakeResult:
        self.statement = statement
        self.params = params
        return FakeResult(self.rows)


def test_sqlalchemy_reader_executes_query_and_maps_rows() -> None:
    session = FakeSession(
        rows=[
            {"sku": "SKU-010", "units": 1, "revenue": "7.50"},
            {"sku": "SKU-011", "units": 2, "revenue": Decimal("10")},
        ],
    )
    reader = SqlAlchemySalesAggregateReader(session=session, currency="USD")

    aggregate = reader.get_sales_aggregate("sales-overview")

    assert "from sales_lines" in session.statement
    assert session.params == {"aggregate_id": "sales-overview"}
    assert aggregate.total_units() == 3
    assert aggregate.total_revenue().amount == Decimal("17.50")
